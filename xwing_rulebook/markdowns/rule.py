from django.urls import reverse
from django.utils.functional import cached_property

from contents.constants import CONTENT_TYPES
from markdowns.base import MarkdownBase
from markdowns.faq import Faq2Markdown
from rules.constants import CLAUSE_TYPES, RULE_TYPES, CLAUSE_GROUPS


class Rule2MarkdownBase(MarkdownBase):
    default_url_name = 'rules:rule'

    def __init__(self, rule, **kwargs):
        super().__init__(**kwargs)
        self.rule = rule

    @staticmethod
    def render_clause_title(clause, content):
        return '' if not content.title or clause.ignore_title else '**{}{}:** '.format(
            content.title, '†' if clause.expansion_related else ''
        )

    @cached_property
    def rule_markdown(self):
        template = (
            '{rule_title}\n'
            '{rule_content}'
            '{huge_ship_related}'
            '{card_errata}'
            '{card_clarification}'
        )

        return template.format(
            rule_title=self.rule_title(),
            rule_content=self.rule_clauses(group__in=[
                CLAUSE_GROUPS.MAIN,
                CLAUSE_GROUPS.IMAGES,
            ]),
            huge_ship_related=self.huge_ship_related_clauses_markdown,
            card_errata=self.card_errata_clauses_markdown,
            card_clarification=self.card_clarification_clauses_markdown,
        )

    def rule_title(self):
        template = '{header_level} {rule_name} {anchor}'
        return template.format(
            header_level='#' * self.header_level,
            rule_name=self.rule.decorated_name,
            anchor='' if not self.anchored else self.render_attrs(
                ids=[self.rule.anchor_id, ],
                classes=[],
                data={
                    'anchor-id': self.rule.anchor_id
                }
            ),
        )

    def rule_clauses(self, **filters):
        template = '{indentation}{prefix}{clause_content}'

        clauses_mds = []
        qs = self.rule.clauses.filter(**filters)

        for clause in qs:
            if clause.current_content.type == CONTENT_TYPES.TEXT:
                clause_md = self.text_content_markdown(clause, clause.current_content)
            elif clause.current_content.type == CONTENT_TYPES.IMAGE:
                clause_md = self.image_content_markdown(clause, clause.current_content)
            else:
                raise NotImplementedError

            md = template.format(
                indentation='    ' * clause.indentation,
                prefix=CLAUSE_TYPES.MARKDOWN_PREFIX_TYPE_MAPPING[clause.type].format(
                    header_level='#' * self.header_level,
                ),
                clause_content=clause_md,
            )

            clauses_mds.append(md)

        return '\n\n'.join(clauses_mds)

    @cached_property
    def main_clauses_markdown(self):
        return self.rule_clauses(group=CLAUSE_GROUPS.MAIN)

    @cached_property
    def image_clauses_markdown(self):
        return self.rule_clauses(group=CLAUSE_GROUPS.IMAGES)

    @cached_property
    def card_errata_clauses_markdown(self):
        template = "\n{header_level} Card errata \n{card_errata_md}\n"

        if self.rule.type != RULE_TYPES.CARD:
            return ''

        card_errata_md = self.rule_clauses(group=CLAUSE_GROUPS.CARD_ERRATA)
        if card_errata_md:
            card_errata_md = template.format(
                header_level='#' * (self.header_level + 1),
                card_errata_md=card_errata_md
            )
        return card_errata_md

    @cached_property
    def card_clarification_clauses_markdown(self):
        template = "\n{header_level} Card Clarifications \n{card_clarification_md}\n"
        if self.rule.type != RULE_TYPES.CARD:
            return ''

        card_clarification_md = self.rule_clauses(group=CLAUSE_GROUPS.CARD_CLARIFICATION)
        if card_clarification_md:
            card_clarification_md = template.format(
                header_level='#' * (self.header_level + 1),
                card_clarification_md=card_clarification_md
            )
        return card_clarification_md

    @cached_property
    def huge_ship_related_clauses_markdown(self):
        template = "\n{header_level} Huge Ships \n{huge_ships_md}\n"
        if self.rule.type == RULE_TYPES.CARD:
            return ''

        huge_ships_md = self.rule_clauses(group=CLAUSE_GROUPS.HUGE_SHIP_RELATED)
        if huge_ships_md:
            huge_ships_md = template.format(
                header_level='#' * (self.header_level + 1),
                huge_ships_md=huge_ships_md
            )
        return huge_ships_md

    def text_content_markdown(self, clause, content):
        file = content.image.static_url if content.image else ''
        clause_content = content.content.replace('<FILE>', file)

        clause_content = self.render_links(clause_content)

        if content.keep_line_breaks:
            clause_content = '\n'.join(
                [clause.indentation * '    ' + c.strip() for c in clause_content.splitlines()]
            )

        template = '{title}{clause_content}'
        if self.anchored:
            template = '{title}{clause_content}{anchor_separation}{anchor}'

        md = template.format(
            title=self.render_clause_title(clause, content),
            clause_content=clause_content,
            anchor_separation='\n' if clause.type != CLAUSE_TYPES.HEADER else ' ',
            anchor='' if not self.anchored else self.render_attrs(
                ids=[clause.anchor_id, ],
                data={
                    'anchor-id': clause.anchor_id,
                    'source-code': content.source.code,
                    'page': '' if content.page is None else content.page,
                    'clause': clause.id,
                    'clause-type': clause.type
                }
            )
        )
        return md

    def image_content_markdown(self, clause, content):
        title = self.render_clause_title(clause, content)
        title_anchor = ''
        if self.anchored and title:
            title_anchor = '\n{indentation}{anchor}\n\n'.format(
                indentation='    ' * clause.indentation,
                anchor=self.render_attrs(
                    ids=[clause.anchor_id, ],
                    classes=['Rule__ImageTitle', ],
                    data={
                        'anchor-id': clause.anchor_id,
                        'source-code': content.source.code,
                        'page': '' if content.page is None else content.page,
                        'clause': clause.id,
                        'clause-type': clause.type
                    }
                )
            )
        image_anchor = ''
        if self.anchored:
            image_anchor = '\n{indentation}{anchor}\n\n'.format(
                indentation='    ' * clause.indentation,
                anchor=self.render_attrs(
                    ids=[clause.anchor_id, ],
                    classes=['Rule__Image', ],
                    data={
                        'anchor-id': clause.anchor_id,
                        'source-code': content.source.code,
                        'page': '' if content.page is None else content.page,
                        'clause': clause.id,
                        'clause-type': clause.type
                    }
                )
            )

        caption = ''
        if content.image.caption:
            caption = '\n{indentation}{caption}'.format(
                indentation='    ' * clause.indentation,
                caption=content.image.caption,
            )

        caption_anchor = ''
        if self.anchored and caption:
            caption_anchor = '\n{indentation}{anchor}'.format(
                indentation='    ' * clause.indentation,
                anchor=self.render_attrs(
                    ids=[clause.anchor_id, ],
                    classes=['Rule__ImageCaption', ],
                    data={
                        'anchor-id': clause.anchor_id,
                        'source-code': content.source.code,
                        'page': '' if content.page is None else content.page,
                        'clause': clause.id,
                        'clause-type': clause.type
                    }
                )
            )

        md = (
            '{title}{title_anchor}'
            '![{alt_text}]({static_url}){image_anchor}'
            '{caption}{caption_anchor}'
        ).format(
            title=title,
            title_anchor=title_anchor,
            alt_text=content.image.alt_text,
            static_url=content.image.static_url,
            image_anchor=image_anchor,
            caption=caption,
            caption_anchor=caption_anchor,
        )

        return md

    def related_rules_as_references(self, rules):

        if not rules.count():
            return ''

        templates = {
            (False, False): '{rule}{expansion_icon}',
            (True, False): '[{rule}{expansion_icon}]({anchor})',
            (False, True): '[{rule}{expansion_icon}]({relative_url})',
            (True, True): '[{rule}{expansion_icon}]({relative_url}{anchor})',
        }

        template = templates[(self.anchored_links, self.linked)]

        url_params = list(self.extra_url_params.items())

        references = ', '.join([
            template.format(
                rule=r.name,
                expansion_icon='' if not r.expansion_rule else '†',
                relative_url=reverse(
                    self.url_name, kwargs=dict([('rule_slug', r.slug)] + url_params)
                ),
                anchor='#{}'.format(r.anchor_id),
            )
            for r in rules
        ])

        return references

    @cached_property
    def related_topics_as_references(self):
        filtered_rules = self.rule.related_rules.filter(type=RULE_TYPES.RULE)
        related_topics_md = self.related_rules_as_references(filtered_rules)
        if related_topics_md:
            related_topics_md = "\n**Related Topics:** {}\n".format(
                related_topics_md
            )
        return related_topics_md

    @cached_property
    def rule_clarifications_as_references(self):
        filtered_rules = self.rule.related_rules.filter(type=RULE_TYPES.RULE_CLARIFICATION)
        rule_clarifications_md = self.related_rules_as_references(filtered_rules)
        if rule_clarifications_md:
            rule_clarifications_md = "\n**Rule Clarifications:** {}\n".format(
                rule_clarifications_md
            )
        return rule_clarifications_md

    @cached_property
    def related_cards_as_references(self):
        filtered_rules = self.rule.related_rules.filter(type=RULE_TYPES.CARD)
        related_cards_md = self.related_rules_as_references(filtered_rules)
        if related_cards_md:
            related_cards_md = "\n**Related Cards:** {}\n".format(
                related_cards_md
            )
        return related_cards_md


class Rule2Markdown(Rule2MarkdownBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.related_rules_helpers = []

        for rule in self.rule.related_rules.all():
            self.related_rules_helpers.append(
                Rule2MarkdownBase(
                    rule,
                    header_level=self.header_level + 2,
                    anchored=self.anchored,
                    linked=self.linked,
                    anchored_links=self.anchored_links,
                    url_name=self.url_name,
                    **self.extra_url_params
                )
            )

        self.faq_helpers = []

        for faq in self.rule.related_faqs.order_by('topic_order', 'order').all():
            self.faq_helpers.append(
                Faq2Markdown(
                    faq,
                    header_level=self.header_level + 2,
                    anchored=self.anchored,
                    linked=self.linked,
                    anchored_links=self.anchored_links,
                    url_name=self.url_name,
                    **self.extra_url_params
                )
            )

    @cached_property
    def rule_clarifications(self):
        return [
            helper for helper in self.related_rules_helpers
            if helper.rule.type == RULE_TYPES.RULE_CLARIFICATION
        ]

    @cached_property
    def rule_clarifications_as_content(self):
        template = "\n{header_level} Rule Clarifications \n{rule_clarifications_mds}\n"

        rule_clarifications = self.rule_clarifications

        if not rule_clarifications:
            return ''

        rule_clarifications_mds = template.format(
            header_level='#' * (self.header_level + 1),
            rule_clarifications_mds='\n\n'.join(
                [helper.rule_markdown() for helper in rule_clarifications]
            )
        )
        return rule_clarifications_mds

    @cached_property
    def rule_related_faqs(self):
        template = "\n{header_level} Related FAQs \n{related_faqs_md}\n"

        if not self.faq_helpers:
            return ''

        faq_mds = template.format(
            header_level='#' * (self.header_level + 1),
            related_faqs_md='\n\n'.join(
                [helper.faq_markdown() for helper in self.faq_helpers]
            )
        )
        return faq_mds
