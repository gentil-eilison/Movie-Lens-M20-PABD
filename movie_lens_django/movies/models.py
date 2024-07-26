from django.db import models
from django.utils.translation import gettext_lazy as _

from movie_lens_django.constants import MEDIUM_SIZED_CHAR_FIELD


class Genre(models.Model):
    name = models.CharField(max_length=MEDIUM_SIZED_CHAR_FIELD, verbose_name=_("Name"))

    class Meta:
        verbose_name = _("Genre")
        verbose_name_plural = _("Genres")

    def __str__(self):
        return self.name
