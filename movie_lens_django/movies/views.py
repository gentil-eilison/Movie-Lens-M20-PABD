from movie_lens_django.core.views import ConcurrentImportView, ImportView

from movie_lens_django.movies.concurrent_import import MoviesConcurrentImport
from movie_lens_django.movies.concurrent_import import MovieTagConcurrentImport
from movie_lens_django.movies.concurrent_import import MovieLinksConcurrentImport


class ImportCSVMovieView(ConcurrentImportView):
    concurrent_import_class = MoviesConcurrentImport
    template_name = "movies/movie_import_form.html"


class ImportCSVMovieTagView(ConcurrentImportView):
    concurrent_import_class = MovieTagConcurrentImport
    template_name = "movies/movie_tag_import_form.html"

class ImportCSVMovieLinksView(ConcurrentImportView):
    concurrent_import_class = MovieLinksConcurrentImport
    template_name = "movies/movie_links_import_form.html"

