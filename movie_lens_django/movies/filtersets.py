import django_filters
from django.db import models

from movie_lens_django.movies.models import Genre
from movie_lens_django.movies.models import Movie


class MovieFilterSet(django_filters.FilterSet):
    title = django_filters.CharFilter(
        label="Título",
        field_name="title",
        lookup_expr="icontains",
    )
    release_year = django_filters.RangeFilter(
        label="Ano de lançamento",
        field_name="release_year",
    )
    rating = django_filters.NumberFilter(
        label="Avaliação mínima",
        field_name="ratings__rating",
        lookup_expr="gte",
    )
    genres = django_filters.ModelMultipleChoiceFilter(
        label="Gênero",
        field_name="genres",
        queryset=Genre.objects.all(),
    )
    ratings_count = django_filters.NumberFilter(
        label="Quantidade mínima de avaliações",
        method="filter_ratings_count",
    )

    class Meta:
        model = Movie
        exclude = [
            "genome_tags",
        ]

    def filter_ratings_count(self, queryset, name, value):
        annotated_queryset = queryset.annotate(count=models.Count("ratings"))
        return annotated_queryset.filter(count__gte=value)
