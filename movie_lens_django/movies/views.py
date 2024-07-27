from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import CreateView

from movie_lens_django.core.models import CSVImportMetaData
from movie_lens_django.movies.forms import MovieCSVImportMetaDataForm


class ImportCSVMovieView(SuccessMessageMixin, CreateView):
    model = CSVImportMetaData
    form_class = MovieCSVImportMetaDataForm
    template_name = "movies/movie_import_form.html"
    success_message = "Importação feita!"
    success_url = "/"
