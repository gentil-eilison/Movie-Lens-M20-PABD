import time

from celery import shared_task
from django.db import connection

from movie_lens_django.constants import READ_CSV_CHUNK_SIZE
from movie_lens_django.core.concurrent_import import ConcurrentImport
from movie_lens_django.genome.models import GenomeTag
from movie_lens_django.movies.models import Movie


class GenomeScoresConcurrentImport(ConcurrentImport):
    @staticmethod
    @shared_task(name="genome-scores-concurrent-import")
    def process_csv_chunk(chunk_data: list[dict], csv_id: int):
        records_added = 0
        errors_count = 0
        tags_ids = set(GenomeTag.objects.values_list("id", flat=True))
        movies_ids = set(Movie.objects.values_list("id", flat=True))
        insert_command = """
        INSERT INTO genome_genomescore(movie_id, genome_tag_id, relevance) VALUES
        """

        start_time = time.time()
        with connection.cursor() as cursor:
            for idx, row in enumerate(chunk_data):
                if row["tagId"] in tags_ids and row["movieId"] in movies_ids:
                    if idx + 1 != READ_CSV_CHUNK_SIZE:
                        insert_command += f"""
                            ({row['movieId']}, {row['tagId']}, {row['relevance']}),
                            """
                    else:
                        insert_command += f"""
                            ({row['movieId']}, {row['tagId']}, {row['relevance']}) ON CONFLICT DO NOTHING;
                            """  # noqa: E501
                else:
                    errors_count += 1
            cursor.execute(insert_command)
            records_added = cursor.rowcount

        end_time = time.time()
        GenomeScoresConcurrentImport.update_csv_metadata.delay(
            csv_id=csv_id,
            inserted_data_count=records_added,
            errors_count=errors_count,
            elasped_time=end_time - start_time,
        )
