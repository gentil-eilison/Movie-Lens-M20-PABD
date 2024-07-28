import abc

from django import forms

from .models import CSVImportMetaData


class CSVImportMetaDataForm(forms.ModelForm):
    class Meta:
        model = CSVImportMetaData
        fields = [
            "csv_file",
        ]


class SimpleCSVImportMetaDataForm(CSVImportMetaDataForm):
    @abc.abstractmethod
    def add_csv_rows(self, filename: str):
        pass

    def save(self, *args, **kwargs):
        instance = super().save(*args, **kwargs)
        records_added, errors_count, elasped_time = self.add_csv_rows(
            instance.csv_file.path,
        )
        instance.inserted_data_count = records_added
        instance.errors_count = errors_count
        instance.upload_time_in_minutes = elasped_time
        instance.save()
        return instance
