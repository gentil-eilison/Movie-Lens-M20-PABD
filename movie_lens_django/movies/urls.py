from django.urls import path

from . import views

app_name = "movies"

urlpatterns = [
    path(
        "csv-import/",
        views.ImportCSVMovieView.as_view(),
        name="csv-import",
    ),
    path(
        "movies-tags-csv-import/",
        views.ImportCSVMovieTagView.as_view(),
        name="movie-tag-csv-import",
    ),
]
