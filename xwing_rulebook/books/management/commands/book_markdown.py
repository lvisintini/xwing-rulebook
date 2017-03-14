from django.core.management.base import BaseCommand
from books.models import Book
from rules.templatetags.related_rules import rules_as_references
from rules.models import RULE_TYPES


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
            book_template = "# {book_name}\n{book_content}\n{sections}"
            section_template = "## {section_title}\n{section_content}\n{rules}\n"
            rule_template = (
                '{title_and_rule}\n{related_topics}{rule_clarifications}{rule_examples}\n'
            )

            sections = []
            for section in book.section_set.all():
                rules = []
                for section_rule in section.sectionrule_set.all():
                    r = section_rule.rule

                    related_topics = r.related_rules.filter(type=RULE_TYPES.RULE)

                    related_topics_md = ''
                    if related_topics.count():
                        related_topics_md = "\n**Related Topics:** {}\n".format(
                            rules_as_references(related_topics, False, False)
                        )

                    rule_clarifications = r.related_rules.filter(type=RULE_TYPES.RULE_CLARIFICATION)

                    rule_clarifications_md = ''
                    if rule_clarifications.count():
                        rule_clarifications_md = "\n**Rule Clarifications:** {}\n".format(
                            rules_as_references(rule_clarifications, False, False)
                        )

                    rule_examples = r.related_rules.filter(type=RULE_TYPES.EXAMPLE)

                    rule_examples_md = ''
                    if rule_examples.count():
                        rule_examples_md = "\n**Examples:** {}\n".format(
                            rules_as_references(rule_examples, False, False)
                        )

                    rules.append(
                        rule_template.format(
                            title_and_rule=r.as_unanchored_markdown(),
                            related_topics=related_topics_md,
                            rule_clarifications=rule_clarifications_md,
                            rule_examples=rule_examples_md,
                        )
                    )
                sections.append(
                    section_template.format(
                        section_title=section.title,
                        section_content=section.content,
                        rules=''.join(rules)
                    )
                )

            book_md = book_template.format(
                book_name=book.name,
                book_content=book.description,
                sections=''.join(sections),
            )

            self.stdout.write(book_md)
