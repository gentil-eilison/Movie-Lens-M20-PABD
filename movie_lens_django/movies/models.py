from django.db import models
from django.utils.translation import gettext_lazy as _

from movie_lens_django.constants import LONG_SIZED_CHAR_FIELD
from movie_lens_django.constants import MEDIUM_SIZED_CHAR_FIELD
from movie_lens_django.genome.models import GenomeTag


class Genre(models.Model):
    name = models.CharField(
        max_length=MEDIUM_SIZED_CHAR_FIELD,
        verbose_name=_("Name"),
        unique=True,
    )

    class Meta:
        verbose_name = _("Genre")
        verbose_name_plural = _("Genres")

    def __str__(self):
        return self.name


class Movie(models.Model):
    title = models.CharField(max_length=LONG_SIZED_CHAR_FIELD, verbose_name=_("Title"))
    release_year = models.PositiveSmallIntegerField(verbose_name=_("Release Year"))
    genres = models.ManyToManyField(to=Genre, verbose_name=_("Genres"))
    genome_tags = models.ManyToManyField(to=GenomeTag, through="MovieGenomeTag")

    class Meta:
        verbose_name = _("Movie")
        verbose_name_plural = _("Movies")

    def __str__(self):
        return self.title


class MovieGenomeTag(models.Model):
    movie = models.ForeignKey(
        Movie,
        on_delete=models.CASCADE,
        related_name="movie_genome_tag",
        verbose_name=_("Movie"),
    )
    genome_tag = models.ForeignKey(
        GenomeTag,
        on_delete=models.CASCADE,
        related_name="movie_genome_tag",
        verbose_name=_("Genome Tag"),
    )
    user_id = models.PositiveIntegerField(verbose_name=_("User ID"))

    class Meta:
        verbose_name = _("Movie Genome Tags By User")
        verbose_name_plural = _("Movie Genome Tags By User")

    def __str__(self):
        return (
            f"Genome Tag: {self.genome_tag.tag} - "
            f"Movie: {self.movie.title} - "
            f"User: {self.user_id}"
        )
