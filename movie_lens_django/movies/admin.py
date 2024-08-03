from django.contrib import admin

from .models import Genre
from .models import Movie

admin.site.register(Movie)
admin.site.register(Genre)
