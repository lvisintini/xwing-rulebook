from rules.helpers import Rule2Markdown
from rules.models import RULE_TYPES


class Book2Markdown:
    def __init__(self, book):
        self.book = book

    def as_single_page(self, anchored, linked, *args, **kwargs):
        book_template = "# {book_name} #\n\n{book_content}\n\n{sections}"
        section_template = "## {section_title} ##\n\n{section_content}\n\n{rules}\n"
        rule_template = (
            '{title_and_rule}\n{related_topics}{rule_clarifications}\n'
        )

        sections = []
        for section in self.book.section_set.all():
            rules = []
            for section_rule in section.sectionrule_set.all():
                r = section_rule.rule

                md_helper = Rule2Markdown(r)

                rules.append(
                    rule_template.format(
                        title_and_rule=md_helper.rule_to_markdown(anchored, 3),
                        related_topics=md_helper.related_topics_references(
                            anchored, linked, *args, **kwargs
                        ),
                        rule_clarifications=md_helper.rule_clarifications_references(
                            anchored, linked, *args, **kwargs
                        ),
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
            book_name=self.book.name,
            book_content=self.book.description,
            sections=''.join(sections),
        )

        return book_md

    def book_related_topics_references(self, rule, section=None):
        filtered_rules = rule.related_rules.filter(type=RULE_TYPES.RULE, id__in=self.book.rule_ids)
        kwargs = {
            'url_name': 'books:rule-in-book',
            'book_slug': self.book.slug,
        }
        if section:
            kwargs['url_name'] = 'books:rule'
            kwargs['section_slug'] = section.slug

        related_topics_md = Rule2Markdown.rules_as_references(
            filtered_rules,
            False,
            True,
            **kwargs
        )

        if related_topics_md:
            related_topics_md = "\n**Related Topics:** {}\n".format(
                related_topics_md
            )
        return related_topics_md
