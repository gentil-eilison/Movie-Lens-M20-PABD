import re

from django.db import IntegrityError
from django.db import connection
from django.db import transaction

from movie_lens_django.core.concurrent_import import ConcurrentImport
from movie_lens_django.movies.models import Genre
from movie_lens_django.movies.models import Movie


class MoviesConcurrentImport(ConcurrentImport):
    @staticmethod
    def __get_title_release_year(title_row: str) -> tuple[str, str]:
        release_year = re.search(r"\(\d{4}\)", title_row)
        if not release_year:
            return title_row, "NULL"

        title = re.search(r".+(?=(\(\d{4}\)))", title_row)
        title = title.group(0).strip()
        release_year = release_year.group(0).replace("(", " ").replace(")", " ").strip()
        return title, release_year

    @staticmethod
    def __get_or_create_genres(genres_row: str) -> list[int]:
        row_genres_names = genres_row.split("|")
        cleaned_genres_names = [genre_name.strip() for genre_name in row_genres_names]
        existing_genres = Genre.objects.filter(name__in=cleaned_genres_names)
        genres_data = {genre.name: genre.id for genre in existing_genres}
        genres_ids = []
        new_genres = []

        for genre_name in cleaned_genres_names:
            if genre_name in genres_data:
                genres_ids.append(genres_data[genre_name])
            else:
                new_genres.append(Genre(name=genre_name))

        if new_genres:
            new_genres_list = Genre.objects.bulk_create(new_genres)
            genres_ids.extend([genre.id for genre in new_genres_list])
        return genres_ids

    @staticmethod
    def process_csv_chunk(chunk_data: list[dict]):
        movies_genres = []
        errors_count = 0
        rows_count = len(chunk_data)
        insert_command = """
        INSERT INTO movies_movie(id, title, release_year) VALUES
        """

        movies_ids = set(Movie.objects.values_list("id", flat=True))
        for idx, row in enumerate(chunk_data):
            title, release_year = MoviesConcurrentImport.__get_title_release_year(
                row["title"],
            )
            genres_ids = MoviesConcurrentImport.__get_or_create_genres(row["genres"])

            if row["movieId"] not in movies_ids:
                title = title.replace("'", "''")
                insert_command += f"""
                ({row["movieId"]}, '{title}', {release_year})
                """
                is_final_row = idx + 1 == rows_count
                if not is_final_row:
                    insert_command += ","
                else:
                    insert_command += "ON CONFLICT DO NOTHING;"
                current_movies_genres = [
                    Movie.genres.through(
                        movie_id=row["movieId"],
                        genre_id=genre_id,
                    )
                    for genre_id in genres_ids
                ]
                movies_genres.extend(current_movies_genres)
        with connection.cursor() as cursor, transaction.atomic():
            try:
                cursor.execute(insert_command)
            except IntegrityError:
                errors_count = cursor.rowcount
            Movie.genres.through.objects.bulk_create(movies_genres)
            return errors_count, cursor.rowcount
