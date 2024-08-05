from django.db import connection
from django.db import transaction

from movie_lens_django.core.concurrent_import import ConcurrentImport
from movie_lens_django.genome.models import GenomeTag
from movie_lens_django.movies.models import Movie


class GenomeScoresConcurrentImport(ConcurrentImport):
    @staticmethod
    def process_csv_chunk(chunk_data: list[dict]):
        errors_count = 0
        tags_ids = set(GenomeTag.objects.values_list("id", flat=True))
        movies_ids = set(Movie.objects.values_list("id", flat=True))
        insert_command = """
        INSERT INTO genome_genomescore(movie_id, genome_tag_id, relevance) VALUES
        """

        chunk_size = len(chunk_data)
        with connection.cursor() as cursor:
            for idx, row in enumerate(chunk_data):
                if row["tagId"] in tags_ids and row["movieId"] in movies_ids:
                    if idx + 1 != chunk_size:
                        insert_command += f"""
                            ({row['movieId']}, {row['tagId']}, {row['relevance']}),
                            """
                    else:
                        insert_command += f"""
                            ({row['movieId']}, {row['tagId']}, {row['relevance']}) ON CONFLICT DO NOTHING;
                            """  # noqa: E501
                else:
                    errors_count += 1
            with transaction.atomic():
                cursor.execute(insert_command)
                rows_affected = cursor.rowcount
                return errors_count, rows_affected
