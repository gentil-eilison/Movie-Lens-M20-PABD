from django import forms

from movie_lens_django.movies.models import Movie
from movie_lens_django.movies.models import MovieGenomeTag


class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ["title", "release_year"]


class MovieTagForm(forms.ModelForm):
    class Meta:
        model = MovieGenomeTag
        fields = ["movie", "genome_tag", "user_id"]
