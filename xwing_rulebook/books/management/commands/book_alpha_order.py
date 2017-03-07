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
            for section in book.section_set.all():
                o = 0
                section_rules = section.sectionrule_set.select_related('rule')
                section_rules = section_rules.order_by('rule__slug')
                for section_rule in section_rules:
                    section_rule.order = o
                    section_rule.save()
                    o += 1
