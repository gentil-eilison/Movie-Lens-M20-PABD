import django_filters

from movie_lens_django.movies.models import Movie


class MovieFilterSet(django_filters.FilterSet):
    title = django_filters.CharFilter(field_name="title", lookup_expr="icontains")
    release_year = django_filters.RangeFilter(field_name="release_year")

    class Meta:
        model = Movie
        fields = ["genres", "genome_tags"]
