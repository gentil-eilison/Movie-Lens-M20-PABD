from movie_lens_django.core.views import ImportView
from movie_lens_django.genome.forms import GenomeTagCSVImportMetaDataForm


class ImportCSVGenomeTagView(ImportView):
    form_class = GenomeTagCSVImportMetaDataForm
    template_name = "genome/genome_tag_form.html"
    success_message = "Importação feita"
