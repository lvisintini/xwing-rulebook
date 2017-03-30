from django.template import Library

from rules.helpers import Rule2Markdown


register = Library()


@register.filter
def rule_as_markdown(rule, level=3):
    return Rule2Markdown(
        rule,
        anchored=False,
        linked=True,
        header_level=level,
    ).rule_to_markdown()


@register.filter
def related_topics_as_rule_linked_list_markdown(rule):
    return Rule2Markdown(
        rule,
        anchored=False,
        linked=True,
    ).related_topics_references()


@register.filter
def filter_related_rules_by_type(rule, rule_type):
    return rule.related_rules.filter(type=rule_type)
