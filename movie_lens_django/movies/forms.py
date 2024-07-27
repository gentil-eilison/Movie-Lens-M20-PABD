import csv
import re
from io import StringIO

from django import forms

from movie_lens_django.core.forms import CSVImportMetaDataBaseForm
from movie_lens_django.movies.models import Movie


class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ["title", "release_year"]


class MovieCSVImportMetaDataForm(CSVImportMetaDataBaseForm):
    def add_csv_rows(self, rows):
        rows = StringIO(rows)
        records_added = 0
        errors = []
        # Generate a dict per row, with the first CSV row being the → keys.
        for row in csv.DictReader(rows, delimiter=","):
            movie_id = row.pop("movieId")

            # Split release year from title
            title_release_year = row.pop("title")
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
                    form.instance.id = movie_id
                    form.instance.title = title
                    form.instance.release_year = release_year
                    form.save()
                    records_added += 1
                else:
                    errors.append(form.errors)

        return records_added, errors

    def save(self, commit=True):  # noqa: FBT002
        instance = super().save(commit=commit)
        file_content = instance.csv_file.read().decode("utf-8")
        self.add_csv_rows(file_content)
        return instance
