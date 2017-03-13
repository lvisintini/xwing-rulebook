from django.utils.safestring import mark_safe
from django.template import Library

from markdown2 import Markdown

from integrations.templatetags.xwing_icons import xwing_icons

register = Library()


@register.simple_tag
def md2html(subject, rulebook=None):
    markdown = Markdown(extras=["tables"])

    if hasattr(subject, 'to_markdown'):
        subject = subject.to_markdown(True, rulebook)

    return mark_safe(xwing_icons(markdown.convert(subject)))

register.filter('md2html', md2html)
