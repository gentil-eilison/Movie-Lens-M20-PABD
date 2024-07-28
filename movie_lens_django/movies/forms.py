from django import forms

from movie_lens_django.movies.models import Movie


class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ["title", "release_year"]
