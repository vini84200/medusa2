from django import template
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe
import misaka as m

register = template.Library()


@register.filter(is_safe=True)
@stringfilter
def md(value):
    rendered_text = mark_safe(m.html(value,
                              extensions=m.EXT_FENCED_CODE,
                              render_flags=m.HTML_ESCAPE))
    return rendered_text
