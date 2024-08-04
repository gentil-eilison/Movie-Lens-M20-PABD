import time

from celery import shared_task

from movie_lens_django.core.concurrent_import import ConcurrentImport
from movie_lens_django.genome.models import GenomeScore
from movie_lens_django.genome.models import GenomeTag
from movie_lens_django.movies.models import Movie


class GenomeScoresConcurrentImport(ConcurrentImport):
    @staticmethod
    @shared_task(name="genome-scores-concurrent-import")
    def process_csv_chunk(chunk_data: list[dict], csv_id: int):
        genome_scores = []
        records_added = 0
        errors_count = 0
        tags_ids = set(GenomeTag.objects.values_list("id", flat=True))
        movies_ids = set(Movie.objects.values_list("id", flat=True))

        start_time = time.time()
        for row in chunk_data:
            if row["tagId"] in tags_ids and row["movieId"] in movies_ids:
                genome_scores.append(
                    GenomeScore(
                        genome_tag_id=row["tagId"],
                        movie_id=row["movieId"],
                        relevance=row["relevance"],
                    ),
                )
                records_added += 1
            else:
                errors_count += 1
        end_time = time.time()

        GenomeScore.objects.bulk_create(genome_scores)
        GenomeScoresConcurrentImport.update_csv_metadata.delay(
            csv_id,
            records_added,
            errors_count,
            end_time - start_time,
        )
