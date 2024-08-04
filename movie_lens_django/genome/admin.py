from django.contrib import admin

from .models import GenomeScore
from .models import GenomeTag

admin.site.register(GenomeTag)
admin.site.register(GenomeScore)
