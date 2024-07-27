# Create your views here.
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import CreateView

from movie_lens_django.core.models import CSVImportMetaData
from movie_lens_django.genome.forms import GenomeTagCSVImportMetaDataForm


class ImportCSVGenomeTagView(SuccessMessageMixin, CreateView):
    model = CSVImportMetaData
    form_class = GenomeTagCSVImportMetaDataForm
    template_name = "genome/genome_tag_form.html"
    success_message = "Importação feita!"
    success_url = "/"
