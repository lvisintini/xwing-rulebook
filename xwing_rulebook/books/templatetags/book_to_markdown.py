from django.template import Library

from books.helpers import Book2Markdown

register = Library()


@register.filter
def book_as_single_page_markdown(book):
    return Book2Markdown(book).as_single_page(anchored=True, linked=False)
