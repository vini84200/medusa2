""" Fields personalizados para Models"""
#  Developed by Vinicius José Fritzen
#  Last Modified 12/04/19 13:17.
#  Copyright (c) 2019  Vinicius José Fritzen and Albert Angel Lanzarini
import json

from django.core.serializers.json import DjangoJSONEncoder
from django.db import models

from escola.widgets import ColorWidget


class ColorField(models.CharField):
    """ Um campo para armazenar uma cor. """
    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 10
        super(ColorField, self).__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        """ Campo no Formulario"""
        kwargs['widget'] = ColorWidget
        return super(ColorField, self).formfield(**kwargs)


class JSONField(models.TextField):
    """Um campo para armazenar JSON."""

    def to_python(self, value):
        if value is None:
            return None

        if value == "":
            return None

        try:
            if isinstance(value, str):
                return json.loads(value)
        except ValueError:
            pass

        return value

    def get_db_prep_save(self,  value, con):
        """Convert our JSON object to a string before we save"""

        if value == "":
            return None

        if isinstance(value, dict):
            value = json.dumps(value, cls=DjangoJSONEncoder)

        return super(JSONField, self).get_db_prep_save(value, con)