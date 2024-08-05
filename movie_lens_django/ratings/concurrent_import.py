import datetime

import pytz
from celery import shared_task
from django.conf import settings
from django.db import connection
from django.db import transaction

from movie_lens_django.core.concurrent_import import ConcurrentImport
from movie_lens_django.movies.models import Movie


class RatingsConcurrentImport(ConcurrentImport):
    @staticmethod
    def format_unix_timestamp(timestamp: str):
        timezone = pytz.timezone(settings.TIME_ZONE)
        timestamp_obj = datetime.datetime.fromtimestamp(timestamp, tz=timezone)
        return timestamp_obj.strftime("%Y-%m-%d %H:%M:%S")

    @staticmethod
    @shared_task(name="process_ratings")
    def process_csv_chunk(chunk_data: list[dict]) -> tuple[int, int]:
        errors_count = 0
        movies_ids = set(Movie.objects.values_list("id", flat=True))
        rows_count = len(chunk_data)
        insert_command = """
        INSERT INTO ratings_rating(rating, "timestamp", movie_id, "user") VALUES
        """

        for idx, row in enumerate(chunk_data):
            if row["movieId"] in movies_ids:
                timestamp = RatingsConcurrentImport.format_unix_timestamp(
                    row["timestamp"],
                )
                insert_command += f"""
                ({row["rating"]}, '{timestamp}', {row["movieId"]}, {row["userId"]})
                """
                is_final_row = idx + 1 == rows_count
                if not is_final_row:
                    insert_command += ","
                else:
                    insert_command += "ON CONFLICT DO NOTHING;"
            else:
                errors_count += 1
        with connection.cursor() as cursor, transaction.atomic():
            cursor.execute(insert_command)
            return errors_count, cursor.rowcount
