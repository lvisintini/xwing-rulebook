from django.core.management.base import BaseCommand

from books.models import Book


class Command(BaseCommand):
    help = 'Provides complete markdown for a book'

    def add_arguments(self, parser):
        parser.add_argument(
            '--book',
            dest='book_code',
            type=str,
            help='The code for the book you want the markdown for.',
        )

    def handle(self, *args, **options):
        book = None
        if options.get('book_code'):
            try:
                book = Book.objects.get(code=options['book_code'])
            except Book.DoesNotExist:
                self.stdout.write(self.style.ERROR(
                    'Failed to load Book'.format(options['book_code'])
                ))

        if book:
            markdown = '\n\n\n'.join([
                section_rule.rule.to_markdown(False)
                for section in book.section_set.all()
                for section_rule in section.sectionrule_set.all()

            ])
            self.stdout.write(markdown)
