from django.contrib import admin

from .models import Genre
from .models import Movie
from .models import MovieGenomeTag
from .models import MovieLinks

admin.site.register(Movie)
admin.site.register(Genre)
admin.site.register(MovieGenomeTag)
admin.site.register(MovieLinks)