""" Widgets personalizados para minha aplicação."""
#  Developed by Vinicius José Fritzen
#  Last Modified 12/04/19 13:19.
#  Copyright (c) 2019  Vinicius José Fritzen and Albert Angel Lanzarini

from django.forms.widgets import Input


class ColorWidget(Input):
    """ Um simples seletor de cor. """
    input_type = 'color'
    template_name = 'escola/forms/widgets/color.html'
