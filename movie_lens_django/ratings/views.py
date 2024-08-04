from movie_lens_django.core.views import ConcurrentImportView

from .concurrent_import import RatingsConcurrentImport


class RatingsConcurrentImportView(ConcurrentImportView):
    concurrent_import_class = RatingsConcurrentImport
    template_name = "ratings/rating_form.html"
    success_message = "Importação iniciada"
