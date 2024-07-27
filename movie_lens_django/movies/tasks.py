import re

import pandas as pd
from celery import group
from celery import shared_task

from movie_lens_django.constants import READ_CSV_CHUNK_SIZE
from movie_lens_django.core.models import CSVImportMetaData


@shared_task
def process_csv_chunk(chunk_data, csv_id: int):
    from movie_lens_django.movies.forms import MovieForm
    from movie_lens_django.movies.models import Movie

    movies = []
    records_added = 0
    errors_count = 0
    for row in chunk_data:
        title_release_year = row["title"]
        title = re.search(r".+(?=(\(\d{4}\)))", title_release_year)
        release_year = re.search(r"\(\d{4}\)", title_release_year)

        if title and release_year:
            title = title.group(0).strip()
            release_year = (
                release_year.group(0).replace("(", " ").replace(")", " ").strip()
            )

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
    csv_data = CSVImportMetaData.objects.get(id=csv_id)
    csv_data.inserted_data_count += records_added
    csv_data.errors_count += errors_count
    csv_data.save()


@shared_task
def import_movies_csv(csv_id: int, filename: str):
    chunk_tasks = []
    with pd.read_csv(filename, chunksize=READ_CSV_CHUNK_SIZE) as reader:
        for chunk in reader:
            chunk_data = chunk.to_dict(orient="records")
            chunk_tasks.append(process_csv_chunk.s(chunk_data, csv_id))

    group(chunk_tasks).apply_async()
