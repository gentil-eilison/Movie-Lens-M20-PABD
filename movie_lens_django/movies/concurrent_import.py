import re
import time

from celery import shared_task

from movie_lens_django.core.concurrent_import import ConcurrentImport
from movie_lens_django.movies.forms import MovieForm
from movie_lens_django.movies.models import Genre
from movie_lens_django.movies.models import Movie


class MoviesConcurrentImport(ConcurrentImport):
    @staticmethod
    def __get_title_release_year(title_row: str) -> tuple[str, str]:
        title = re.search(r".+(?=(\(\d{4}\)))", title_row)
        release_year = re.search(r"\(\d{4}\)", title_row)
        if title and release_year:
            title = title.group(0).strip()
            release_year = (
                release_year.group(0).replace("(", " ").replace(")", " ").strip()
            )
            return title, release_year
        return "", ""

    @staticmethod
    def __create_genres(genres_row: str) -> None:
        row_genres_names = genres_row.split("|")
        cleaned_genres_names = [genre_name.strip() for genre_name in row_genres_names]
        for genre_name in cleaned_genres_names:
            Genre.objects.get_or_create(
                name=genre_name,
                defaults={"name": genre_name},
            )

    @staticmethod
    @shared_task
    def process_csv_chunk(chunk_data: list[dict], csv_id: int):
        movies = []
        records_added = 0
        errors_count = 0
        start_time = time.time()
        for row in chunk_data:
            title, release_year = MoviesConcurrentImport.__get_title_release_year(
                row["title"],
            )
            MoviesConcurrentImport.__create_genres(row["genres"])

            if title and release_year:
                form = MovieForm(data={"title": title, "release_year": release_year})
                # Check to see if the row data is valid.
                if form.is_valid():
                    # Row data is valid so save the record.
                    movie_exists = Movie.objects.filter(id=row["movieId"]).first()
                    if not movie_exists:
                        movies.append(
                            Movie(
                                id=row["movieId"],
                                title=title,
                                release_year=release_year,
                            ),
                        )
                        records_added += 1
                else:
                    errors_count += 1
        Movie.objects.bulk_create(movies)
        end_time = time.time()
        elasped_time = end_time - start_time
        MoviesConcurrentImport.update_csv_metadata.delay(
            csv_id,
            records_added,
            errors_count,
            elasped_time,
        )
