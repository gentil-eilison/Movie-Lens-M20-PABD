from django.db import models
from django.utils.translation import gettext_lazy as _

from movie_lens_django.constants import MEDIUM_SIZED_CHAR_FIELD


class GenomeTag(models.Model):
    tag = models.CharField(max_length=MEDIUM_SIZED_CHAR_FIELD, verbose_name=_("Tag"))

    class Meta:
        verbose_name = _("Genome Tag")
        verbose_name_plural = _("Genome Tags")

    def __str__(self):
        return self.tag
