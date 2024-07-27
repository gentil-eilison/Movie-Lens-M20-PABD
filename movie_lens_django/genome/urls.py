from django.urls import path

from . import views

app_name = "genome"

urlpatterns = [
    path(
        "genome-tag-csv-import/",
        views.ImportCSVGenomeTagView.as_view(),
        name="genome-tag-csv-import",
    ),
]
