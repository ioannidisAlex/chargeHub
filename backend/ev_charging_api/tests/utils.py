from django.db import models
from hypothesis.extra.django import from_model


def generate_single(m: models.Model, **kw):
    field_strategies = {
        field.name: generate_single(field.related_model)
        for field in m._meta.concrete_fields
        if isinstance(field, (models.ForeignKey, models.OneToOneField))
    }
    field_strategies.update(kw)
    return from_model(m, **field_strategies)
