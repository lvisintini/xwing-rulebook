from django.utils.safestring import mark_safe
from django.template import Library

from markdown2 import Markdown

register = Library()


def md2html(subject):
    markdown = Markdown()

    if hasattr(subject, 'to_markdown'):
        subject = subject.to_markdown()

    return mark_safe(markdown.convert(subject))

register.filter('md2html', md2html)


def indentation(level):
    return mark_safe('    ' * level)

register.filter('indentation', indentation)
