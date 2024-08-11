import importlib
import re
import sys
import time

import pandas as pd
from celery import shared_task
from django.db import IntegrityError
from django.db import connection
from django.db import transaction

from movie_lens_django.constants import READ_CSV_CHUNK_SIZE
from movie_lens_django.core.concurrent_import import ConcurrentImport
from movie_lens_django.core.concurrent_import import CSVImportMetaData
from movie_lens_django.core.mixins import FormatUnixTimeStampMixin
from movie_lens_django.genome.models import GenomeTag
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
                errors_count = rows_count
            Movie.genres.through.objects.bulk_create(movies_genres)
            return errors_count, cursor.rowcount


class MovieTagConcurrentImport(ConcurrentImport, FormatUnixTimeStampMixin):
    @staticmethod
    def process_csv_chunk(chunk_data: list[dict]):
        errors_count = 0
        tags = {
            tag_name: tag_id
            for tag_id, tag_name in GenomeTag.objects.values_list("id", "tag")
        }
        sync_genome_tags_pks_sequence_command = """
            SELECT SETVAL('public."genome_genometag_id_seq"', COALESCE(MAX(id), 1))
            FROM public."genome_genometag";
        """
        movies_ids = set(Movie.objects.values_list("id", flat=True))
        insert_command = """
        INSERT INTO movies_moviegenometag (user_id, genome_tag_id, movie_id, timestamp)
        VALUES
        """
        insert_tag_command = """
            INSERT INTO genome_genometag (tag) VALUES (%s) RETURNING id;
        """
        values = []
        with connection.cursor() as cursor, transaction.atomic():
            cursor.execute(sync_genome_tags_pks_sequence_command)
            for row in chunk_data:
                row_tag = row["tag"].strip()
                row_movie_id = row["movieId"]

                if row_movie_id in movies_ids:
                    if row_tag in tags:
                        tag_id = tags[row_tag]
                    else:
                        cursor.execute(insert_tag_command, [row_tag])
                        tag_id = cursor.fetchone()[0]
                        tags[row_tag] = tag_id
                    timestamp = MovieTagConcurrentImport.format_unix_timestamp(
                        row["timestamp"],
                    )
                    values.append(
                        f"({row['userId']}, {tag_id}, {row_movie_id}, '{timestamp}')",
                    )
                else:
                    errors_count += 1
        if values:
            insert_command += ", ".join(values)
            insert_command += " ON CONFLICT DO NOTHING;"
            with connection.cursor() as cursor, transaction.atomic():
                try:
                    cursor.execute(insert_command)
                except IntegrityError:
                    errors_count = len(chunk_data)
                rows_affected = cursor.rowcount
                return errors_count, rows_affected
        else:
            return errors_count, 0


class MovieLinksConcurrentImport(ConcurrentImport):
    @staticmethod
    def process_csv_chunk(chunk_data: list[dict]):
        errors_count = 0
        movies_ids = set(Movie.objects.values_list("id", flat=True))
        insert_command = """
        INSERT INTO movies_movielinks (movie_id, imdb_id, tmdb_id) VALUES
        """
        values = []
        with connection.cursor() as cursor, transaction.atomic():
            for row in chunk_data:
                row_movie_id = row["movieId"]
                if int(row_movie_id) in movies_ids:
                    imdb_id = row["imdbId"] if row["imdbId"] else "NULL"
                    tmdb_id = row["tmdbId"] if row["tmdbId"] else "NULL"
                    values.append(f"({row_movie_id}, '{imdb_id}', '{tmdb_id}')")
                else:
                    errors_count += 1
        if values:
            insert_command += ", ".join(values)
            insert_command += " ON CONFLICT DO NOTHING;"
            with connection.cursor() as cursor, transaction.atomic():
                try:
                    cursor.execute(insert_command)
                except IntegrityError:
                    errors_count = len(chunk_data)
                rows_affected = cursor.rowcount
                sys.stdout.write(str(rows_affected))
                return errors_count, rows_affected
        else:
            return errors_count, 0

    @staticmethod
    @shared_task(name="call-import-links-task")
    def call_import_task(concurrent_import_class_name: str, csv_id: int, filename: str):
        module_name, class_name = concurrent_import_class_name.rsplit(".", 1)
        module = importlib.import_module(module_name)
        concurrent_import_class = getattr(module, class_name)

        total_errors, total_rows = 0, 0
        start_time = time.time()
        with pd.read_csv(
            filename,
            chunksize=READ_CSV_CHUNK_SIZE,
            quotechar='"',
            na_values=None,
            keep_default_na=False,
            dtype=str,
        ) as reader:
            for chunk in reader:
                chunk_data = chunk.to_dict(orient="records")
                sys.stdout.write(len(chunk_data))
                errors_count, rows_count = concurrent_import_class.process_csv_chunk(
                    chunk_data,
                )
                total_rows += rows_count
                total_errors += errors_count
        end_time = time.time()

        csv_import = CSVImportMetaData.objects.get(id=csv_id)
        csv_import.upload_time_in_seconds = end_time - start_time
        csv_import.errors_count = total_errors
        csv_import.inserted_data_count = total_rows
        csv_import.save()
