from django.core.management.base import BaseCommand

from rule.models import RuleBook


class Command(BaseCommand):
    help = 'Provides complete markdown for a book'

    def add_arguments(self, parser):
        parser.add_argument(
            '--rulebook',
            dest='rulebook_code',
            type=str,
            help='The code for the Rulebook you want the markdown for.',
        )

        parser.add_argument(
            '--separate-paragraphs',
            action='store_true',
            dest='separate_paragraphs',
            default=False,
            help='Provide separate paragraphs instead of whole rules.',
        )

    def handle(self, *args, **options):
        rb = None
        if options.get('rulebook_code'):
            try:
                rb = RuleBook.objects.get(code=options['rulebook_code'])
            except RuleBook.DoesNotExist:
                self.stdout.write(self.style.ERROR(
                    'Failed to load RuleBook'.format(options['rulebook_code'])
                ))

        if rb:
            markdown = '\n\n\n'.join([
                r.to_markdown(False)
                for section in rb.booksection_set.all()
                for r in section.rules.order_by('id').all()

            ])
            self.stdout.write(markdown)
