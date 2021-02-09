from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def validate_positive(value):
    if value <= 0:
        raise ValidationError(_("Den ftais esy , upirxe arnitiki timi se pedio pou pairnei thetikous"))
    return value

def validate_language(value):
    if "fuck" in value:
        raise ValidationError(_("Hey watch your language"))
    return value
