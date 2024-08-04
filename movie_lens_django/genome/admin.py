from django.contrib import admin

from .models import GenomeScore
from .models import GenomeTag


admin.site.register(GenomeScore)

@admin.register(GenomeTag)
class GenomeTagAdmin(admin.ModelAdmin):
    search_fields = ["tag"]
