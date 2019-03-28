""" Fields personalizados para Models"""
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