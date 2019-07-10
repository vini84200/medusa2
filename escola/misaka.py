from misaka import html

from .settings import MARKDOWNX_MARKDOWN_EXTENSIONS


def to_html(content):
    md = html(
        text=content,
        extensions=MARKDOWNX_MARKDOWN_EXTENSIONS,
        render_flags=('skip-html',)
    )
    return md
