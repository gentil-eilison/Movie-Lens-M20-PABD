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
        "tags-by-user/csv-import/",
        views.ImportCSVMovieTagView.as_view(),
        name="tags-by-user-csv-import",
    ),
    path(
        "links/csv-import/",
        views.ImportCSVMovieLinksView.as_view(),
        name="links-csv-import",
    ),
]
