from rules.helpers import Rule2Markdown
from rules.models import RULE_TYPES


class BookRule2Markdown(Rule2Markdown):
    def __init__(self, book, rule, **kwargs):
        self.book = book
        super().__init__(rule, **kwargs)

    def related_topics_as_references(self):
        filtered_rules = self.rule.related_rules.filter(
            type=RULE_TYPES.RULE,
            id__in=self.book.rule_ids
        )
        related_topics_md = self.related_rules_as_references(filtered_rules)
        if related_topics_md:
            related_topics_md = "\n**Related Topics:** {}\n".format(
                related_topics_md
            )
        return related_topics_md

    def rule_clarifications_as_references(self):
        filtered_rules = self.rule.related_rules.filter(
            type=RULE_TYPES.RULE_CLARIFICATION,
            id__in=self.book.rule_ids
        )
        rule_clarifications_md = self.related_rules_as_references(filtered_rules)
        if rule_clarifications_md:
            rule_clarifications_md = "\n**Rule Clarifications:** {}\n".format(
                rule_clarifications_md
            )
        return rule_clarifications_md


class Book2Markdown:
    def __init__(self, book, **kwargs):
        self.book = book

        self.anchored = kwargs.pop('anchored', False)
        self.linked = kwargs.pop('linked', False)
        self.anchored_links = kwargs.pop('anchored_links', False)
        self.extra_url_params = kwargs

    def as_single_page(self):
        book_template = "# {book_name}\n\n{book_content}\n\n{sections}"
        section_template = "## {section_title}\n\n{section_content}\n\n{rules}\n"
        rule_template = (
            '{title_and_rule}\n{related_topics}{rule_clarifications}\n'
        )

        sections = []
        for section in self.book.section_set.all():
            rules = []
            for section_rule in section.sectionrule_set.all():
                r = section_rule.rule

                md_helper = Rule2Markdown(
                    r,
                    anchored=self.anchored,
                    linked=self.linked,
                    anchored_links=self.anchored_links,
                    header_level=3,
                    **self.extra_url_params
                )

                rules.append(
                    rule_template.format(
                        title_and_rule=md_helper.rule_markdown(),
                        related_topics=md_helper.related_topics_as_references(),
                        rule_clarifications=md_helper.rule_clarifications_as_references(),
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
