from django.urls import path

from . import views

app_name = "movies"

urlpatterns = [
    path(
        "csv-import/",
        views.ImportCSVMovieView.as_view(),
        name="csv-import",
    ),
]
