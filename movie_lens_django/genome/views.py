# Create your views here.
from django.views.generic.edit import CreateView

from movie_lens_django.core.forms import CSVImportMetaDataForm
from movie_lens_django.genome.models import GenomeTag


class ImportCSVGenomeTagView(CreateView):
    model = GenomeTag
    form = CSVImportMetaDataForm
