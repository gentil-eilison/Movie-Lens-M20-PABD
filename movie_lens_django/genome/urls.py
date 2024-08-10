from django.urls import path

from . import views

app_name = "genome"

urlpatterns = [
    path(
        "import-genome-tags/",
        views.ImportCSVGenomeTagView.as_view(),
        name="import-genome-tags",
    ),
    path(
        "import-scores/",
        views.ImportCSVGenomeScoreView.as_view(),
        name="import-scores",
    ),
]
