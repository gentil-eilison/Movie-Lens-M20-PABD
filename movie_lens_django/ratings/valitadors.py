from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

VALID_RATINGS = (0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0)


def validate_rating(value: float):
    if value not in VALID_RATINGS:
        raise ValidationError(
            _("%(value)s is a valid rating"),
            params={"value": value},
        )
