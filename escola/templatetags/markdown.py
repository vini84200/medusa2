from django import template
from django.template.defaultfilters import stringfilter
import misaka as m

register = template.Library()

@register.filter(is_safe=True)
@stringfilter
def gfm(value):
    rendered_text = m.html(value,
                           extensions=m.EXT_FENCED_CODE,
                           render_flags=m.HTML_ESCAPE)
    return rendered_text