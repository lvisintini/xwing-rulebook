from django.core.management.base import BaseCommand

from books.models import Book
from books.helpers import Book2Markdown


class Command(BaseCommand):
    help = 'Provides complete markdown for a book'

    def add_arguments(self, parser):
        parser.add_argument(
            'book_code',
            type=str,
            help='The code for the book you want the markdown for.'
        )

    def handle(self, *args, **options):
        book = None

        try:
            book = Book.objects.get(code=options.get('book_code'))
        except Book.DoesNotExist:
            self.stdout.write(self.style.ERROR(
                'Failed to load Book'.format(options.get('book_code'))
            ))

        if book:
            self.stdout.write(Book2Markdown(book).as_single_page(anchored=False, linked=False))
