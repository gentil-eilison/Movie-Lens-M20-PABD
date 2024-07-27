import csv
from io import StringIO

from django import forms

from movie_lens_django.core.forms import CSVImportMetaDataBaseForm
from movie_lens_django.genome.models import GenomeTag


class GenomeTagForm(forms.ModelForm):
    class Meta:
        model = GenomeTag
        fields = ["tag"]


class GenomeTagCSVImportMetaDataForm(CSVImportMetaDataBaseForm):
    def add_csv_rows(self, rows):
        rows = StringIO.StringIO(rows)
        records_added = 0
        errors = []
        # Generate a dict per row, with the first CSV row being the → keys.
        for row in csv.DictReader(rows, delimiter=","):
            # Bind the row data to the PurchaseForm.
            tag_id = row.pop("tagId")
            form = GenomeTagForm(row)
            # Check to see if the row data is valid.
            if form.is_valid():
                # Row data is valid so save the record.
                form.instance.id = tag_id
                form.save()
                records_added += 1
            else:
                errors.append(form.errors)
        return records_added, errors
