from math import isinf, isnan

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_positive(value):
    if value < 0:
        raise ValidationError(_("Oups,non-positive values are not allowed"))
    if isinf(value):
        raise ValidationError(_("Oups, infinite values are not allowed"))
    if isnan(value):
        raise ValidationError(_("Oups, NaN values are not allowed"))
    return value
