from django.core.management.base import BaseCommand

from books.models import Book


class Command(BaseCommand):
    help = 'Provides complete markdown for a book'

    def add_arguments(self, parser):
        parser.add_argument(
            'book_code',
            type=str,
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
            for section in book.section_set.all():
                o = 0
                section_rules = section.sectionrule_set.select_related('rule')
                section_rules = section_rules.order_by('rule__slug')
                for section_rule in section_rules:
                    section_rule.order = o
                    section_rule.save()
                    o += 1
