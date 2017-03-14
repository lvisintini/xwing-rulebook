from django.template import Library
from django.urls import reverse

register = Library()


@register.simple_tag
def rules_as_references(rules, add_anchors=False, add_links=False, url_name='rules:rule', **kwargs):
        if not rules.count():
            return ''

        templates = {
            (False, False): '{rule}{expansion_icon}',
            (True, False): '[{rule}{expansion_icon}](#{anchor})',
            (False, True): '[{rule}{expansion_icon}]({relative_url})',
            (True, True): '[{rule}{expansion_icon}]({relative_url}#{anchor})',
        }

        template = templates[(add_anchors, add_links)]

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


@register.filter(name='related_rules')
def filter_related_rules(rule, **kwargs):
    return rule.related_rules.filter(**kwargs)
