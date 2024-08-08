from django import forms

from movie_lens_django.movies.models import Movie
from movie_lens_django.movies.models import MovieGenomeTag
from movie_lens_django.movies.models import MovieLinks


class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ["title", "release_year"]


class MovieTagForm(forms.ModelForm):
    class Meta:
        model = MovieGenomeTag
        fields = ["movie", "genome_tag", "user_id"]

class MovieLinksForm(forms.ModelForm):
    class Meta:
        model = MovieLinks
        fields = ["movie_id", "imdb_id", "tmdb_id"]