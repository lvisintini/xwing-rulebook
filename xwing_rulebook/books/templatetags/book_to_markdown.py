from django.template import Library

from books.helpers import Book2Markdown
from rules.helpers import Rule2Markdown
from utils.templatetags.markdown import md2html

register = Library()


@register.filter
def book_as_single_page_markdown(book):
    return Book2Markdown(book, anchored=True, linked=False).as_single_page()


@register.simple_tag(takes_context=True)
def related_topics_as_book_linked_list_markdown(context, rule):
    md = Book2Markdown(
        context['book'],
        linked=True
    ).book_related_topics_references(rule, context.get('section'))
    return md2html(md)
