from itertools import groupby
from collections import OrderedDict

from django.shortcuts import render
from django.http.response import Http404

from rules.models import Rule
from rules.constants import RULE_TYPES, CARD_TYPES
from markdowns.rule import Rule2Markdown


def rule(request, rule_slug=None):
    try:
        rule = Rule.objects.prefetch_related('clauses__available_contents').get(slug=rule_slug)
    except Rule.DoesNotExist:
        raise Http404

    helper = Rule2Markdown(
        rule,
        anchored=True,
        linked=True,
        anchored_links=False,
        header_level=1,
    )

    context = {
        'rule': rule,
        'rule2markdown': helper
    }
    return render(request, 'rule.html', context)


def rules_index(request):
    qs = Rule.objects.order_by('type_order', 'card_type_order', 'name')

    grouped_rules = groupby(
        qs.all(),
        key=lambda r: (
            (
                r.type if r.type != RULE_TYPES.RULE_CLARIFICATION else RULE_TYPES.RULE,
                dict(RULE_TYPES.as_choices)[
                    r.type if r.type != RULE_TYPES.RULE_CLARIFICATION else RULE_TYPES.RULE
                ]
            ),
            (
                r.card_type_order,
                dict(CARD_TYPES.as_choices)[r.card_type],
            )
        )
    )

    rules_by_type = OrderedDict()
    for key, group in grouped_rules:
        if key[0] not in rules_by_type:
            rules_by_type[key[0]] = OrderedDict()
        rules_by_type[key[0]][key[1]] = list(group)

    context = {
        'rules_by_type': rules_by_type,
    }
    return render(request, 'index.html', context)
