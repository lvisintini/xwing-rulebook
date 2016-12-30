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
                rbr.rule.to_markdown(False)
                for rbr in rb.rulebookrule_set.order_by('order').all()
            ])
            self.stdout.write(markdown)
