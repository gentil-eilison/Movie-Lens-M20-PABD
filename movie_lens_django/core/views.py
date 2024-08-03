from django.contrib.messages.views import SuccessMessageMixin
from django.forms import BaseForm
from django.http.response import HttpResponse
from django.views.generic import CreateView

from movie_lens_django.core.forms import CSVImportMetaDataForm
from movie_lens_django.core.models import CSVImportMetaData


class ImportView(SuccessMessageMixin, CreateView):
    model = CSVImportMetaData
    form_class = CSVImportMetaDataForm
    success_message = "Importação iniciada"
    success_url = "/"


class ConcurrentImportView(ImportView):
    concurrent_import_class = None

    def form_valid(self, form: BaseForm) -> HttpResponse:
        form.save()
        self.concurrent_import_class.call_import_task(
            csv_id=form.instance.id,
            filename=form.instance.csv_file.path,
        )
        return super().form_valid(form)
