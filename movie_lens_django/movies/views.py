from movie_lens_django.core.views import ConcurrentImportView
from movie_lens_django.movies.concurrent_import import MoviesConcurrentImport
from movie_lens_django.movies.concurrent_import import MovieTagConcurrentImport


class ImportCSVMovieView(ConcurrentImportView):
    concurrent_import_class = MoviesConcurrentImport
    template_name = "movies/movie_import_form.html"


class ImportCSVMovieTagView(ConcurrentImportView):
    concurrent_import_class = MovieTagConcurrentImport
    template_name = "movies/movie_tag_import_form.html"
