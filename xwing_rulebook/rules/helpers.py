from django.urls import reverse

from rules.models import RULE_TYPES, CLAUSE_TYPES, CLAUSE_GROUPS
from contents.models import TextContent, ImageContent


class Rule2MarkdownBase:
    default_url_name = 'rules:rule'

    def __init__(self, rule, **kwargs):
        self.rule = rule

        self.header_level = kwargs.pop('header_level', 3)
        self.anchored = kwargs.pop('anchored', False)
        self.linked = kwargs.pop('linked', False)
        self.anchored_links = kwargs.pop('anchored_links', False)
        self.url_name = kwargs.pop('url_name', self.default_url_name)
        self.extra_url_params = kwargs

    @staticmethod
    def render_attrs(ids=None, classes=None, data=None):
        ids = ids or []
        classes = classes or []
        data = data or {}

        template = "{{: {ids} {classes} {data} }}"

        return template.format(
            ids=' '.join(['#{}'.format(x) for x in ids]) if ids else '',
            classes=' '.join(['.{}'.format(x) for x in classes]) if classes else '',
            data=' '.join(
                ['data-{}="{}"'.format(k, v) for k, v in data.items() if v or v == 0]
            ) if data else '',
        )

    @staticmethod
    def render_clause_title(clause, content):
        return '' if not content.title or clause.ignore_title else '**{}{}:** '.format(
            content.title, '†' if clause.expansion_related else ''
        )

    def render_link(self, link):
        templates = {
            (False, False, False): '{text}',
            (False, False, True): '[{text}]({url})',
            (False, True, False): '{text}',
            (False, True, True): '[{text}]({url})',

            (True, False, False): '{rule}{expansion_icon}',
            (True, False, True): '[{rule}{expansion_icon}]({relative_url})',
            (True, True, False): '[{rule}{expansion_icon}](#{anchor})',
            (True, True, True): '[{rule}{expansion_icon}]({relative_url}#{anchor})',
        }

        template = templates[(bool(link.rule), self.anchored_links, self.linked)]
        url_params = list(self.extra_url_params.items())

        return template.format(
            rule=link.rule.name,
            expansion_icon='†' if link.rule and link.rule.expansion_rule else '',
            relative_url=reverse(
                self.url_name, kwargs=dict([('rule_slug', link.rule.slug)] + url_params)
            ) if link.rule else '',
            anchor=link.rule.anchor_id if link.rule else '',
            url=link.url,
            text=link.text
        )

    def rule_markdown(self):
        return '{rule_title}\n{rule_content}{card_errata}{card_clarification}'.format(
            rule_title=self.rule_title(),
            rule_content=self.rule_clauses(group__in=[
                CLAUSE_GROUPS.MAIN,
                CLAUSE_GROUPS.IMAGES,
            ]),
            card_errata=self.card_errata_clauses_markdown(),
            card_clarification=self.card_clarification_clauses_markdown(),
        )

    def rule_title(self):
        template = '{header_level} {rule_name}{expansion_rule} {anchor}'
        return template.format(
            header_level='#' * self.header_level,
            rule_name=self.rule.name,
            expansion_rule='' if not self.rule.expansion_rule else ' †',
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

        for clause in self.rule.clauses.filter(**filters):

            content = clause.current_content.get_real_instance()
            if isinstance(content, TextContent):
                clause_md = self.text_content_markdown(clause, content)
            elif isinstance(content, ImageContent):
                clause_md = self.image_content_markdown(clause, content)
            else:
                raise NotImplementedError

            md = template.format(
                indentation='    ' * clause.indentation,
                prefix=CLAUSE_TYPES.MARKDOWN_PREFIX_TYPE_MAPPING[clause.type],
                clause_content=clause_md,
            )

            clauses_mds.append(md)

        return '\n\n'.join(clauses_mds)

    def main_clauses_markdown(self):
        return self.rule_clauses(group=CLAUSE_GROUPS.MAIN)

    def image_clauses_markdown(self):
        return self.rule_clauses(group=CLAUSE_GROUPS.IMAGES)

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

    def text_content_markdown(self, clause, content):
        file = content.image.static_url if content.image else ''
        clause_content = content.content.replace('<FILE>', file)

        for l in content.links.all():
            clause_content = clause_content.replace(
                '<LINK:{}>'.format(l.alias), self.render_link(l)
            )

        if content.keep_line_breaks:
            clause_content = '\n'.join(
                [clause.indentation * '    ' + c.strip() for c in clause_content.splitlines()]
            )

        template = '{title}{clause_content}{anchor}'

        md = template.format(
            title=self.render_clause_title(clause, content),
            clause_content=clause_content,
            anchor='' if not self.anchored else '\n' + self.render_attrs(
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
            (True, False): '[{rule}{expansion_icon}](#{anchor})',
            (False, True): '[{rule}{expansion_icon}]({relative_url})',
            (True, True): '[{rule}{expansion_icon}]({relative_url}#{anchor})',
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
                anchor=r.anchor_id,
            )
            for r in rules
        ])

        return references

    def related_topics_as_references(self):
        filtered_rules = self.rule.related_rules.filter(type=RULE_TYPES.RULE)
        related_topics_md = self.related_rules_as_references(filtered_rules)
        if related_topics_md:
            related_topics_md = "\n**Related Topics:** {}\n".format(
                related_topics_md
            )
        return related_topics_md

    def rule_clarifications_as_references(self):
        filtered_rules = self.rule.related_rules.filter(type=RULE_TYPES.RULE_CLARIFICATION)
        rule_clarifications_md = self.related_rules_as_references(filtered_rules)
        if rule_clarifications_md:
            rule_clarifications_md = "\n**Rule Clarifications:** {}\n".format(
                rule_clarifications_md
            )
        return rule_clarifications_md


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
                    url_name=self.url_name,
                    **self.extra_url_params
                )
            )

    def rule_clarifications(self):
        return [
            helper for helper in self.related_rules_helpers
            if helper.rule.type == RULE_TYPES.RULE_CLARIFICATION
        ]

    def rule_clarifications_as_content(self):
        template = "\n{header_level} Rule Clarifications \n{rule_clarifications_mds}\n"

        rule_clarifications = self.rule_clarifications()

        if not rule_clarifications:
            return ''

        rule_clarifications_mds = template.format(
            header_level='#' * (self.header_level + 1),
            rule_clarifications_mds='\n\n'.join(
                [helper.rule_markdown() for helper in rule_clarifications]
            )
        )
        return rule_clarifications_mds
