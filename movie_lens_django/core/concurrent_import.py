import abc
import importlib

import pandas as pd
from celery import group
from celery import shared_task

from movie_lens_django.constants import READ_CSV_CHUNK_SIZE
from movie_lens_django.core.models import CSVImportMetaData


class ConcurrentImport(abc.ABC):
    @staticmethod
    @abc.abstractmethod
    def process_csv_chunk(chunk_data: list[dict], csv_id: int):
        error_msg = "You must implement 'process_csv_chunk' method"
        raise NotImplementedError(error_msg)

    @staticmethod
    @shared_task
    def call_import_task(concurrent_import_class_name: str, csv_id: int, filename: str):
        module_name, class_name = concurrent_import_class_name.rsplit(".", 1)
        module = importlib.import_module(module_name)
        concurrent_import_class = getattr(module, class_name)
        chunk_tasks = []
        with pd.read_csv(filename, chunksize=READ_CSV_CHUNK_SIZE) as reader:
            for chunk in reader:
                chunk_data = chunk.to_dict(orient="records")
                chunk_tasks.append(
                    concurrent_import_class.process_csv_chunk.s(chunk_data, csv_id),
                )

        group(chunk_tasks).apply_async()

    @staticmethod
    @shared_task
    def update_csv_metadata(
        csv_id: int,
        inserted_data_count: int,
        errors_count: int,
        elasped_time: float,
    ):
        csv_data = CSVImportMetaData.objects.get(id=csv_id)
        csv_data.inserted_data_count += inserted_data_count
        csv_data.errors_count += errors_count
        csv_data.upload_time_in_minutes = elasped_time
        csv_data.save()
