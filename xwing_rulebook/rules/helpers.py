from django.urls import reverse
from django.conf import settings
from django.contrib.staticfiles.templatetags.staticfiles import static

from rules.models import RULE_TYPES, CLAUSE_TYPES


class Rule2Markdown:
    def __init__(self, rule):
        self.rule = rule

    def as_anchored_markdown(self):
        return self.rule_to_markdown(True)

    def as_unanchored_markdown(self):
        return self.rule_to_markdown(False)

    def rule_to_markdown(self, anchored, header_level=3):
        template = '#' * header_level + ' {anchor}{rule_name}{expansion_rule}\n{clauses}'
        anchor_template = '<a id="{anchor_id}"></a>'

        return template.format(
            anchor='' if not anchored else anchor_template.format(anchor_id=self.rule.anchor_id),
            rule_name=self.rule.name,
            expansion_rule='' if not self.rule.expansion_rule else ' †',
            clauses=self.clauses_to_markdown(anchored)
        )

    def clauses_to_markdown(self, anchored):
        template = '{indentation}{prefix}{anchor}{title}{content}'
        anchor_template = '<a class="SourceReference" id="{anchor_id}">' \
                          '{source_code}{page}{clause}</a>'

        clauses_mds = []

        for clause in self.rule.clauses.all():

            content = clause.current_content

            file = ''
            if content.file:
                file = static(content.file.replace(settings.STATICFILES_DIRS[0], ''))

            md = template.format(
                indentation='    ' * clause.indentation,
                prefix=CLAUSE_TYPES.MARKDOWN_PREFIX_TYPE_MAPPING[clause.type],
                anchor='' if not anchored else anchor_template.format(
                    anchor_id=clause.anchor_id,
                    source_code=content.source.code,
                    page='' if content.page is None else ' (Page {})'.format(content.page),
                    clause=' [{}]'.format(clause.id)
                ),
                title='' if not content.title or clause.ignore_title else '**{}{}:** '.format(
                    content.title, '†' if clause.expansion_related else ''
                ),
                content=content.content.replace('<FILE>', file),
            )

            clauses_mds.append(md)

        return '\n\n'.join(clauses_mds)

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

    def rule_examples_references(self, *args, **kwargs):
        filtered_rules = self.rule.related_rules.filter(type=RULE_TYPES.EXAMPLE)
        rule_examples_md = self.rules_as_references(filtered_rules, *args, **kwargs)
        if rule_examples_md:
            rule_examples_md = "\n**Examples:** {}\n".format(
                rule_examples_md
            )
        return rule_examples_md
