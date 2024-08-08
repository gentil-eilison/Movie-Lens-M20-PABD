from typing import Any

from django.db.models.query import QuerySet
from django_filters.views import FilterView

from movie_lens_django.core.views import ConcurrentImportView
from movie_lens_django.movies.concurrent_import import MoviesConcurrentImport
from movie_lens_django.movies.concurrent_import import MovieTagConcurrentImport
from movie_lens_django.movies.filtersets import MovieFilterSet
from movie_lens_django.movies.models import Movie


class ImportCSVMovieView(ConcurrentImportView):
    concurrent_import_class = MoviesConcurrentImport
    template_name = "movies/movie_import_form.html"


class ImportCSVMovieTagView(ConcurrentImportView):
    concurrent_import_class = MovieTagConcurrentImport
    template_name = "movies/movie_tag_import_form.html"


class MoviesListView(FilterView):
    template_name = "movies/movie_list.html"
    filterset_class = MovieFilterSet
    context_object_name = "objects"
    model = Movie
    paginate_by = 25

    def get_queryset(self) -> QuerySet[Any]:
        queryset = super().get_queryset()
        if not self.request.GET:
            return queryset.none()
        return queryset
