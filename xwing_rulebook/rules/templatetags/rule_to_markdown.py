from django.template import Library

from rules.helpers import Rule2Markdown


register = Library()


@register.filter
def rule_as_anchored_markdown(rule, level=3):
    return Rule2Markdown(rule).rule_to_markdown(True, level)


@register.filter
def rule_as_unanchored_markdown(rule, level=3):
    return Rule2Markdown(rule).rule_to_markdown(False, level)


@register.filter
def related_topics_as_rule_linked_list_markdown(rule):
    return Rule2Markdown(rule).related_topics_references(False, True)


@register.filter
def filter_related_rules_by_type(rule, rule_type):
    return rule.related_rules.filter(type=rule_type)
