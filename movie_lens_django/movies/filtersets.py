import django_filters
from django.db import models

from movie_lens_django.movies.models import Genre
from movie_lens_django.movies.models import Movie


class MovieFilterSet(django_filters.FilterSet):
    title = django_filters.CharFilter(
        label="Title",
        field_name="title",
        lookup_expr="icontains",
    )
    release_year = django_filters.RangeFilter(
        label="Release Year Range",
        field_name="release_year",
    )
    rating = django_filters.NumberFilter(
        label="Minimum Rating",
        field_name="ratings__rating",
        lookup_expr="gte",
        distinct=True,
    )
    genres = django_filters.ModelMultipleChoiceFilter(
        label="Genres",
        field_name="genres",
        queryset=Genre.objects.all(),
    )
    ratings_count = django_filters.NumberFilter(
        label="Min Ratings Count",
        method="filter_ratings_count",
        distinct=True,
    )
    user_id = django_filters.NumberFilter(
        label="User ID",
        method="filter_user_id",
        distinct=True,
    )

    class Meta:
        model = Movie
        exclude = [
            "genome_tags",
        ]

    def filter_ratings_count(self, queryset, name, value):
        annotated_queryset = queryset.annotate(count=models.Count("ratings"))
        return annotated_queryset.filter(count__gte=value)

    def filter_user_id(self, queryset, name, value):
        return queryset.filter(ratings__user=value)
