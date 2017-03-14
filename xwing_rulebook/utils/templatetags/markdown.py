from django.utils.safestring import mark_safe
from django.template import Library

from markdown2 import Markdown

from integrations.templatetags.xwing_icons import xwing_icons

register = Library()


def md2html(subject):
    markdown = Markdown(extras=["tables"])
    return mark_safe(xwing_icons(markdown.convert(subject)))

register.filter('md2html', md2html)
