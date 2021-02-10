from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_positive(value):
    if value < 0:
        raise ValidationError(_("Oups,non-positive values are not allowed"))
    return value


def validate_language(value):
    if "fuck" in value:
        raise ValidationError(_("Please be polite"))
    return value
