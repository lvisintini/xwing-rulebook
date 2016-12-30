from django.utils.safestring import mark_safe
from django.template import Library

from markdown2 import Markdown

register = Library()


def md2html(subject):
    markdown = Markdown(extras=["tables"])

    if hasattr(subject, 'to_markdown'):
        subject = subject.to_markdown()

    return mark_safe(markdown.convert(subject))

register.filter('md2html', md2html)


def indentation(level):
    return mark_safe('    ' * level)

register.filter('indentation', indentation)


def format_paragraph(paragraph):
    text = paragraph.text
    if paragraph.format.get('expansion_rule', False):
        text = text.replace(":**", "†:**", 1)
    return mark_safe(text)

register.filter('format_paragraph', format_paragraph)