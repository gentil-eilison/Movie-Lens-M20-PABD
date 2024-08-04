from django.urls import path

from . import views

app_name = "ratings"

urlpatterns = [
    path(
        "import-ratings/",
        views.RatingsConcurrentImportView.as_view(),
        name="import-ratings",
    ),
]
