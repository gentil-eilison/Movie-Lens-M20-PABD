from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_positive(value: float):
    if value < 0:
        raise ValidationError(
            _("%(value)s must be positive"),
            params={"value": value},
        )
