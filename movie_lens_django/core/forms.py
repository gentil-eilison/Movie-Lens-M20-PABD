from django import forms

from movie_lens_django.core.models import CSVImportMetaData


class CSVImportMetaDataBaseForm(forms.ModelForm):
    class Meta:
        model = CSVImportMetaData
        fields = [
            "csv_file",
        ]

    def add_csv_rows(self, rows):
        pass
