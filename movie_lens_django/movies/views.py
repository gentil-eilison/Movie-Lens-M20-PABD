from django.views.generic import DetailView
from django.views.generic import ListView
from django_filters.views import FilterView

from movie_lens_django.core.views import ConcurrentImportView
from movie_lens_django.movies.concurrent_import import MovieLinksConcurrentImport
from movie_lens_django.movies.concurrent_import import MoviesConcurrentImport
from movie_lens_django.movies.concurrent_import import MovieTagConcurrentImport
from movie_lens_django.movies.filtersets import MovieFilterSet
from movie_lens_django.movies.models import Movie
from movie_lens_django.movies.services.ombd_service import OmdbService
from movie_lens_django.movies.services.tmdb_service import TmdbService


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


class MovieDetailView(DetailView):
    model = Movie
    template_name = "movies/movie_detail.html"
    context_object_name = "movie"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        omdb_service = OmdbService()
        tmdb_service = TmdbService()
        movie = self.get_object()
        context["imdb_data"] = omdb_service.get_movie(movie.get_imdb_id())
        context["tmdb_data"] = tmdb_service.get_movie(movie.get_tmdb_id())
        return context
