from django.contrib import admin

from .models import Genre
from .models import Movie
from .models import MovieGenomeTag

admin.site.register(Movie)
admin.site.register(Genre)
admin.site.register(MovieGenomeTag)
