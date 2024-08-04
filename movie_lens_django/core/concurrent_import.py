import abc
import importlib
import time

import pandas as pd
from celery import shared_task

from movie_lens_django.constants import READ_CSV_CHUNK_SIZE
from movie_lens_django.core.models import CSVImportMetaData


class ConcurrentImport(abc.ABC):
    @staticmethod
    @abc.abstractmethod
    def process_csv_chunk(chunk_data: list[dict]) -> tuple[int, int]:
        error_msg = "You must implement 'process_csv_chunk' method"
        raise NotImplementedError(error_msg)

    @staticmethod
    @shared_task
    def call_import_task(concurrent_import_class_name: str, csv_id: int, filename: str):
        module_name, class_name = concurrent_import_class_name.rsplit(".", 1)
        module = importlib.import_module(module_name)
        concurrent_import_class = getattr(module, class_name)

        total_errors, total_rows = 0, 0
        start_time = time.time()
        with pd.read_csv(filename, chunksize=READ_CSV_CHUNK_SIZE) as reader:
            for chunk in reader:
                chunk_data = chunk.to_dict(orient="records")
                errors_count, rows_count = concurrent_import_class.process_csv_chunk(
                    chunk_data,
                )
                total_rows += rows_count
                total_errors += errors_count
        end_time = time.time()

        csv_import = CSVImportMetaData.objects.get(id=csv_id)
        csv_import.upload_time_in_minutes = end_time - start_time
        csv_import.errors_count = total_errors
        csv_import.inserted_data_count = total_rows
        csv_import.save()
