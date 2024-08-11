from django.contrib.messages.views import SuccessMessageMixin
from django.forms import BaseForm
from django.http.response import HttpResponse
from django.views.generic import CreateView
from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic import TemplateView

from movie_lens_django.core.forms import CSVImportMetaDataForm
from movie_lens_django.core.models import CSVImportMetaData


class ImportCSVsLinksView(TemplateView):
    template_name = "core/import_csvs_links.html"


class ImportView(SuccessMessageMixin, CreateView):
    model = CSVImportMetaData
    form_class = CSVImportMetaDataForm
    success_message = "Importação iniciada"
    success_url = "/"


class ConcurrentImportView(ImportView):
    concurrent_import_class = None

    def form_valid(self, form: BaseForm) -> HttpResponse:
        form.save()
        self.concurrent_import_class.call_import_task.delay(
            concurrent_import_class_name=f"{self.concurrent_import_class.__module__}.{self.concurrent_import_class.__name__}",
            csv_id=form.instance.id,
            filename=form.instance.csv_file.path,
        )
        return super().form_valid(form)


class CSVListView(ListView):
    model = CSVImportMetaData
    template_name = "core/imported_csvs_list.html"
    context_object_name = "csvs"


class CSVDetailView(DetailView):
    model = CSVImportMetaData

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["upload_done"] = self.get_object().upload_status == "Done"
        return context
