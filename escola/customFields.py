""" Fields personalizados para Models"""
#  Developed by Vinicius José Fritzen
#  Last Modified 12/04/19 13:17.
#  Copyright (c) 2019  Vinicius José Fritzen and Albert Angel Lanzarini

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