from django.db import models
from django.utils.translation import gettext_lazy as _

from movie_lens_django.constants import LONG_SIZED_CHAR_FIELD

from . import validators


class GenomeTag(models.Model):
    tag = models.CharField(max_length=LONG_SIZED_CHAR_FIELD, verbose_name=_("Tag"))

    class Meta:
        verbose_name = _("Genome Tag")
        verbose_name_plural = _("Genome Tags")

    def __str__(self):
        return self.tag


class GenomeScore(models.Model):
    relevance = models.FloatField(
        verbose_name=_("Relevance"),
        validators=[validators.validate_positive],
    )
    movie = models.ForeignKey(
        verbose_name=_("Movie"),
        to="movies.Movie",
        on_delete=models.CASCADE,
    )
    genome_tag = models.ForeignKey(
        verbose_name=_("Genome Tag"),
        to=GenomeTag,
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = _("Genome Score")
        verbose_name_plural = _("Genome Scores")
        constraints = [
            models.UniqueConstraint(
                fields=["movie", "genome_tag"],
                name="genome_score_movie_genome_tag_unique_together",
            ),
        ]

    def __str__(self):
        return (
            f"Movie: {self.movie.title} - "
            f"Genome Tag: {self.genome_tag.tag} - "
            f"Relevance: {self.relevance}"
        )
