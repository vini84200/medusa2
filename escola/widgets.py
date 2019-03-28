""" Widgets personalizados para minha aplicação."""
from django.forms.widgets import Input


class ColorWidget(Input):
    """ Um simples seletor de cor. """
    input_type = 'color'
    template_name = 'escola/forms/widgets/color.html'
