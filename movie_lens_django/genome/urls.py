from django.urls import path

from . import views

app_name = "genome"

urlpatterns = [
    path(
        "csv-import/",
        views.ImportCSVGenomeTagView.as_view(),
        name="csv-import",
    ),
]