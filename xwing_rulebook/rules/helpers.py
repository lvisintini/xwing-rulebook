from django.urls import reverse

from rules.models import RULE_TYPES, CLAUSE_TYPES, CLAUSE_ALIGNMENT
from contents.models import TextContent, ImageContent


class Rule2Markdown:
    def __init__(self, rule):
        self.rule = rule

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

    def as_anchored_markdown(self):
        return self.rule_to_markdown(True)

    def as_unanchored_markdown(self):
        return self.rule_to_markdown(False)

    def rule_to_markdown(self, anchored, header_level=3):
        template = '{header_level} {rule_name}{expansion_rule} {header_level} {anchor}\n{clauses}'

        return template.format(
            header_level='#' * header_level,
            rule_name=self.rule.name,
            expansion_rule='' if not self.rule.expansion_rule else ' †',
            clauses=self.clauses_to_markdown(anchored),
            anchor='' if not anchored else self.attrs_render(
                ids=[self.rule.anchor_id, ],
                classes=[],
                data={
                    'anchor-id': self.rule.anchor_id
                }
            ),
        )

    def clauses_to_markdown(self, anchored):
        template = '{indentation}{prefix}{title}{clause_content}'

        clauses_mds = []

        for clause in self.rule.clauses.all():

            content = clause.current_content.get_real_instance()
            if isinstance(content, TextContent):
                clause_md = self.text_content_markdown(clause, content, anchored)
            elif isinstance(content, ImageContent):
                clause_md = self.image_content_markdown(clause, content, anchored)
            else:
                raise NotImplementedError

            md = template.format(
                indentation='    ' * clause.indentation,
                prefix=CLAUSE_TYPES.MARKDOWN_PREFIX_TYPE_MAPPING[clause.type],
                title='' if not content.title or clause.ignore_title else '**{}{}:** '.format(
                    content.title, '†' if clause.expansion_related else ''
                ),
                clause_content=clause_md,
            )

            clauses_mds.append(md)

        return '\n\n'.join(clauses_mds)

    def text_content_markdown(self, clause, content, anchored):
        file = content.image.static_url if content.image else ''
        clause_content = content.content.replace('<FILE>', file)

        if content.keep_line_breaks:
            clause_content = '\n'.join(
                [clause.indentation * '    ' + c.strip() for c in clause_content.splitlines()]
            )

        classes = []
        if clause.alignment == CLAUSE_ALIGNMENT.RIGHT:
            classes.append('u-text-right')
        if clause.alignment == CLAUSE_ALIGNMENT.CENTER:
            classes.append('u-text-center')

        template = '{clause_content}{anchor}'

        md = template.format(
            clause_content=clause_content,
            anchor='' if not anchored else '\n' + self.attrs_render(
                ids=[clause.anchor_id, ],
                classes=classes,
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

    def image_content_markdown(self, clause, content, anchored):

        classes = []
        if clause.alignment == CLAUSE_ALIGNMENT.RIGHT:
            classes.extend(['u-flex', 'u-flex-right'])
        if clause.alignment == CLAUSE_ALIGNMENT.CENTER:
            classes.extend(['u-flex', 'u-flex-center'])

        md = '![alt_text]({static_url}){caption}{anchor}'.format(
            static_url=content.image.static_url,
            alt_text=content.image.alt_text,
            caption='\n{indentation}{caption}'.format(
                caption=content.image.caption,
                indentation='    ' * clause.indentation,
            ) if content.image.caption else '',
            anchor='' if not anchored else '\n' + self.attrs_render(
                ids=[clause.anchor_id, ],
                classes=classes,
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

    @staticmethod
    def rules_as_references(rules, anchored=False, linked=False, url_name='rules:rule', **kwargs):

        if not rules.count():
            return ''

        templates = {
            (False, False): '{rule}{expansion_icon}',
            (True, False): '[{rule}{expansion_icon}](#{anchor})',
            (False, True): '[{rule}{expansion_icon}]({relative_url})',
            (True, True): '[{rule}{expansion_icon}]({relative_url}#{anchor})',
        }

        template = templates[(anchored, linked)]

        url_params = list(kwargs.items())

        references = ', '.join([
            template.format(
                rule=r,
                expansion_icon='' if not r.expansion_rule else '†',
                relative_url=reverse(url_name, kwargs=dict([('rule_slug', r.slug)] + url_params)),
                anchor=r.anchor_id,
            )
            for r in rules
        ])

        return references

    def related_topics_references(self, *args, **kwargs):
        filtered_rules = self.rule.related_rules.filter(type=RULE_TYPES.RULE)
        related_topics_md = self.rules_as_references(filtered_rules, *args, **kwargs)
        if related_topics_md:
            related_topics_md = "\n**Related Topics:** {}\n".format(
                related_topics_md
            )
        return related_topics_md

    def rule_clarifications_references(self, *args, **kwargs):
        filtered_rules = self.rule.related_rules.filter(type=RULE_TYPES.RULE_CLARIFICATION)
        rule_clarifications_md = self.rules_as_references(filtered_rules, *args, **kwargs)
        if rule_clarifications_md:
            rule_clarifications_md = "\n**Rule Clarifications:** {}\n".format(
                rule_clarifications_md
            )
        return rule_clarifications_md
