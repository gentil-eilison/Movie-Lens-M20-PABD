from movie_lens_django.core.views import ConcurrentImportView
from movie_lens_django.movies.concurrent_import import MoviesConcurrentImport


class ImportCSVMovieView(ConcurrentImportView):
    concurrent_import_class = MoviesConcurrentImport
    template_name = "movies/movie_import_form.html"
