from django.db import models
from django.utils.translation import gettext_lazy as _

from movie_lens_django.movies.models import Movie

from . import valitadors


class Rating(models.Model):
    rating = models.FloatField(
        verbose_name=_("Rating"),
        validators=[valitadors.validate_rating],
    )
    timestamp = models.DateTimeField(verbose_name=_("Timestamp"))
    movie = models.ForeignKey(
        verbose_name=_("Movie"),
        to=Movie,
        on_delete=models.CASCADE,
        related_name="ratings",
    )
    user = models.PositiveIntegerField(verbose_name=_("User ID"))

    class Meta:
        verbose_name = _("Rating")
        verbose_name_plural = _("Ratings")
        indexes = [
            models.Index(
                fields=["movie_id"],
                include=["rating"],
                name="rating_movie_id_index",
            ),
        ]

    def __str__(self):
        return (
            f"Movie: {self.movie.title} - "
            f"User: {self.user} - "
            f"Rating: {self.rating} - "
        )
