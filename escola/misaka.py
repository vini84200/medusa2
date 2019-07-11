from misaka import html
from django.utils.safestring import mark_safe
from MedusaII.settings import MARKDOWNX_MARKDOWN_EXTENSIONS


def to_html(content):
    md = html(
        text=content,
        extensions=MARKDOWNX_MARKDOWN_EXTENSIONS,
        render_flags=('skip-html',)
    )
    return md


def to_safe_html(content):
    return mark_safe(to_html(content))


def to_space_safe_html(content):
    return mark_safe('<br>' + to_html(content))
