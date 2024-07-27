import time

import pandas as pd
from django import forms

from movie_lens_django.constants import READ_CSV_CHUNK_SIZE
from movie_lens_django.core.forms import CSVImportMetaDataBaseForm
from movie_lens_django.genome.models import GenomeTag


class GenomeTagForm(forms.ModelForm):
    class Meta:
        model = GenomeTag
        fields = ["tag"]


class GenomeTagCSVImportMetaDataForm(CSVImportMetaDataBaseForm):
    def add_csv_rows(self, filename: str):
        records_added = 0
        errors_count = 0
        genome_tags = []
        with pd.read_csv(filename, chunksize=READ_CSV_CHUNK_SIZE) as reader:
            start_time = time.time()
            for chunk in reader:
                data_frame = pd.DataFrame(chunk)
                for _, row in data_frame.iterrows():
                    form = GenomeTagForm(data={"tag": row["tag"]})
                    if form.is_valid():
                        gnome_tag_exists = GenomeTag.objects.filter(
                            id=row["tagId"],
                        ).first()
                        if not gnome_tag_exists:
                            genome_tags.append(
                                GenomeTag(id=row["tagId"], tag=row["tag"]),
                            )
                            records_added += 1
                    else:
                        errors_count += 1
                GenomeTag.objects.bulk_create(genome_tags)
            end_time = time.time()
        elapsed_time = end_time - start_time
        return records_added, errors_count, elapsed_time

    def save(self, commit=True):  # noqa: FBT002
        instance = super().save(commit=commit)
        records_added, errors_count, elasped_time = self.add_csv_rows(
            instance.csv_file.path,
        )
        instance.inserted_data_count = records_added
        instance.errors_count = errors_count
        instance.upload_time_in_minutes = elasped_time
        instance.save()
        return instance
