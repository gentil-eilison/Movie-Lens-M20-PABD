from django.urls import path

from movie_lens_django.core import views

app_name = "core"

urlpatterns = [
    path("detail/<int:pk>/", views.CSVDetailView.as_view(), name="csv-detail"),
    path("list/", views.CSVListView.as_view(), name="csvs-list"),
    path("import-csvs/", views.ImportCSVsLinksView.as_view(), name="import-csvs"),
]
