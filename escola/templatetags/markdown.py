import misaka as m
from django import template
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe

from MedusaII.settings import MARKDOWNX_MARKDOWN_EXTENSIONS

register = template.Library()


@register.filter(is_safe=True)
@stringfilter
def md(value):
    rendered_text = mark_safe(m.html(value,
                                     extensions=MARKDOWNX_MARKDOWN_EXTENSIONS,
                                     render_flags=('skip-html',)))
    return rendered_text
