from django.urls import reverse

from rules.models import RULE_TYPES, CLAUSE_TYPES
from contents.models import TextContent, ImageContent


class Rule2Markdown:
    def __init__(self, rule, **kwargs):
        self.rule = rule

        self.header_level = kwargs.pop('header_level', 3)
        self.anchored = kwargs.pop('anchored', False)
        self.linked = kwargs.pop('linked', False)
        self.url_name = kwargs.pop('url_name', 'rules:rule')
        self.extra_url_params = kwargs

    @staticmethod
    def attrs_render(ids=None, classes=None, data=None):
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
    def title_render(clause, content):
        return '' if not content.title or clause.ignore_title else '**{}{}:** '.format(
            content.title, '†' if clause.expansion_related else ''
        )

    def link_render(self, link):
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

        template = templates[(bool(link.rule), self.anchored, self.linked)]
        url_params = list(self.extra_url_params.items())
        r = link.rule

        return template.format(
            rule=link.rule,
            expansion_icon='†' if r and r.expansion_rule else '',
            relative_url=reverse(
                self.url_name, kwargs=dict([('rule_slug', r.slug)] + url_params)
            ) if r else '',
            anchor=r.anchor_id if r else '',
            url=link.url,
            text=link.text
        )

    def rule_to_markdown(self):
        template = '{header_level} {rule_name}{expansion_rule} {anchor}\n{clauses}'

        return template.format(
            header_level='#' * self.header_level,
            rule_name=self.rule.name,
            expansion_rule='' if not self.rule.expansion_rule else ' †',
            clauses=self.clauses_to_markdown(),
            anchor='' if not self.anchored else self.attrs_render(
                ids=[self.rule.anchor_id, ],
                classes=[],
                data={
                    'anchor-id': self.rule.anchor_id
                }
            ),
        )

    def clauses_to_markdown(self):
        template = '{indentation}{prefix}{clause_content}'

        clauses_mds = []

        for clause in self.rule.clauses.all():

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

    def text_content_markdown(self, clause, content):
        file = content.image.static_url if content.image else ''
        clause_content = content.content.replace('<FILE>', file)

        for l in content.links.all():
            clause_content = clause_content.replace(
                '<LINK:{}>'.format(l.alias), self.link_render(l)
            )

        if content.keep_line_breaks:
            clause_content = '\n'.join(
                [clause.indentation * '    ' + c.strip() for c in clause_content.splitlines()]
            )

        template = '{title}{clause_content}{anchor}'

        md = template.format(
            title=self.title_render(clause, content),
            clause_content=clause_content,
            anchor='' if not self.anchored else '\n' + self.attrs_render(
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
        title = self.title_render(clause, content)
        title_anchor = ''
        if self.anchored and title:
            title_anchor = '\n{indentation}{anchor}'.format(
                indentation='    ' * clause.indentation,
                anchor=self.attrs_render(
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
            image_anchor = '\n{indentation}{anchor}'.format(
                indentation='    ' * clause.indentation,
                anchor=self.attrs_render(
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
                anchor=self.attrs_render(
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
            '{title}{title_anchor}\n\n'
            '![alt_text]({static_url}){image_anchor}\n\n'
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

    def rules_as_references(self, rules):

        if not rules.count():
            return ''

        templates = {
            (False, False): '{rule}{expansion_icon}',
            (True, False): '[{rule}{expansion_icon}](#{anchor})',
            (False, True): '[{rule}{expansion_icon}]({relative_url})',
            (True, True): '[{rule}{expansion_icon}]({relative_url}#{anchor})',
        }

        template = templates[(self.anchored, self.linked)]

        url_params = list(self.extra_url_params.items())

        references = ', '.join([
            template.format(
                rule=r,
                expansion_icon='' if not r.expansion_rule else '†',
                relative_url=reverse(
                    self.url_name, kwargs=dict([('rule_slug', r.slug)] + url_params)
                ),
                anchor=r.anchor_id,
            )
            for r in rules
        ])

        return references

    def related_topics_references(self):
        filtered_rules = self.rule.related_rules.filter(type=RULE_TYPES.RULE)
        related_topics_md = self.rules_as_references(filtered_rules)
        if related_topics_md:
            related_topics_md = "\n**Related Topics:** {}\n".format(
                related_topics_md
            )
        return related_topics_md

    def rule_clarifications_references(self):
        filtered_rules = self.rule.related_rules.filter(type=RULE_TYPES.RULE_CLARIFICATION)
        rule_clarifications_md = self.rules_as_references(filtered_rules)
        if rule_clarifications_md:
            rule_clarifications_md = "\n**Rule Clarifications:** {}\n".format(
                rule_clarifications_md
            )
        return rule_clarifications_md
