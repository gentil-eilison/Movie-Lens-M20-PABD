from django.urls import path

from movie_lens_django.core.views import CSVDetailView

urlpatterns = [
    path("detail/<int:pk>/", CSVDetailView.as_view(), name="csv-detail"),
]
