from django.urls import path

from . import views

app_name = "movies"

urlpatterns = [
    path(
        "import-movies/",
        views.ImportCSVMovieView.as_view(),
        name="import-movies",
    ),
    path(
        "import-tags-by-user/",
        views.ImportCSVMovieTagView.as_view(),
        name="import-tags-by-user",
    ),
    path(
        "import-links/",
        views.ImportCSVMovieLinksView.as_view(),
        name="import-links",
    ),
    path("list/", views.MoviesListView.as_view(), name="movie-list"),
]
