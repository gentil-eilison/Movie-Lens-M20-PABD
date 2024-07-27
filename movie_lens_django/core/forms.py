from django import forms

from .models import CSVImportMetaData


class CSVImportMetaDataBaseForm(forms.ModelForm):
    class Meta:
        model = CSVImportMetaData
        fields = [
            "csv_file",
        ]
