import time

from celery import shared_task
from django.db import IntegrityError

from movie_lens_django.core.concurrent_import import ConcurrentImport
from movie_lens_django.genome.models import GenomeTag
from movie_lens_django.movies.forms import MovieTagForm
from movie_lens_django.movies.models import Movie
from movie_lens_django.movies.models import MovieGenomeTag


# need to decrease this time
class MovieTagConcurrentImport(ConcurrentImport):
    @staticmethod
    def __get_or_create_movie(genres_row: str) -> list[int]:
        try:
            row_movie_id = int(genres_row)
            movie, created = Movie.objects.get_or_create(
                pk=row_movie_id,
            )
            if created or movie:
                return movie
        except (IntegrityError, ValueError):
            pass
        return None

    @staticmethod
    def __get_or_create_genome_tag(genres_row: str) -> list[int]:
        try:
            row_name_tag = genres_row
            genome_tag, created = GenomeTag.objects.get_or_create(
                tag=row_name_tag,
            )
            if created or genome_tag:
                return genome_tag
        except (IntegrityError, ValueError):
            pass
        return None

    @staticmethod
    @shared_task
    def process_csv_chunk(chunk_data: list[dict], csv_id: int):
        movie_tags = []
        records_added = 0
        errors_count = 0
        start_time = time.time()

        for row in chunk_data:
            movie = MovieTagConcurrentImport.__get_or_create_movie(
                row["movieId"],
            )
            tag = MovieTagConcurrentImport.__get_or_create_genome_tag(row["tag"])

            if movie and tag:
                form = MovieTagForm(
                    data={
                        "movie": movie,
                        "genome_tag": tag,
                        "user_id": row["userId"],
                    },
                )
                # Check to see if the row data is valid.
                if form.is_valid():
                    # Row data is valid so save the record.
                    movie_exists = MovieGenomeTag.objects.filter(
                        movie=movie,
                        genome_tag=tag,
                        user_id=row["userId"],
                    ).first()
                    if not movie_exists:
                        movie_tags.append(
                            MovieGenomeTag(
                                movie=movie,
                                genome_tag=tag,
                                user_id=row["userId"],
                            ),
                        )
                        records_added += 1
                else:
                    errors_count += 1
        MovieGenomeTag.objects.bulk_create(movie_tags)
        end_time = time.time()
        elapsed_time = end_time - start_time
        MovieTagConcurrentImport.update_csv_metadata.delay(
            csv_id,
            records_added,
            errors_count,
            elapsed_time,
        )
