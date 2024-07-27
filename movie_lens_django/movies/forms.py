from django import forms

from movie_lens_django.core.forms import CSVImportMetaDataBaseForm
from movie_lens_django.movies.models import Movie
from movie_lens_django.movies.tasks import import_movies_csv


class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ["title", "release_year"]


class MovieCSVImportMetaDataForm(CSVImportMetaDataBaseForm):
    def save(self, commit=True):  # noqa: FBT002
        instance = super().save(commit=commit)
        import_movies_csv.delay(csv_id=instance.id, filename=instance.csv_file.path)
        return instance
