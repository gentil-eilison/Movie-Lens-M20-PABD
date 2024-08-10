from django.views.generic import ListView
from django_filters.views import FilterView

from movie_lens_django.core.views import ConcurrentImportView
from movie_lens_django.movies.concurrent_import import MovieLinksConcurrentImport
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


class ImportCSVMovieLinksView(ConcurrentImportView):
    concurrent_import_class = MovieLinksConcurrentImport
    template_name = "movies/movie_links_import_form.html"


class MoviesListView(FilterView, ListView):
    model = Movie
    queryset = Movie.objects.all().prefetch_related("genome_tags", "genres")
    filterset_class = MovieFilterSet
    template_name = "movies/movie_list.html"
    context_object_name = "objects"
    paginate_by = 25
