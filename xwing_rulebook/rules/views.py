from itertools import groupby
from collections import OrderedDict, defaultdict

from django.shortcuts import render
from django.http.response import Http404
from django.db import models

from rules.models import Rule, RULE_TYPES, CARD_TYPES
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
    qs = Rule.objects

    qs = qs.annotate(
        type_order=models.Case(
            models.When(
                type=RULE_TYPES.RULE,
                then=RULE_TYPES.as_list.index(RULE_TYPES.RULE)
            ),
            models.When(
                type=RULE_TYPES.RULE_CLARIFICATION,
                then=RULE_TYPES.as_list.index(RULE_TYPES.RULE)
            ),
            models.When(
                type=RULE_TYPES.CARD,
                then=RULE_TYPES.as_list.index(RULE_TYPES.CARD)
            ),
            default=100,
            output_field=models.IntegerField()
        )
    )

    qs = qs.annotate(
        card_type_order=models.Case(
            models.When(
                card_type=CARD_TYPES.NOT_APPLICABLE,
                then=CARD_TYPES.as_list.index(CARD_TYPES.NOT_APPLICABLE)
            ),
            models.When(
                card_type=CARD_TYPES.DAMAGE_ORG,
                then=CARD_TYPES.as_list.index(CARD_TYPES.DAMAGE_ORG)
            ),
            models.When(
                card_type=CARD_TYPES.DAMAGE_TFA,
                then=CARD_TYPES.as_list.index(CARD_TYPES.DAMAGE_TFA)
            ),
            models.When(
                card_type=CARD_TYPES.CONDITION,
                then=CARD_TYPES.as_list.index(CARD_TYPES.CONDITION)
            ),
            models.When(
                card_type=CARD_TYPES.PILOT,
                then=CARD_TYPES.as_list.index(CARD_TYPES.PILOT)
            ),
            models.When(
                card_type=CARD_TYPES.UPGRADE,
                then=CARD_TYPES.as_list.index(CARD_TYPES.UPGRADE)
            ),
            default=100,
            output_field=models.IntegerField()
        )
    )

    qs = qs.order_by('type_order', 'card_type_order', 'name')

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

    rules_by_type = defaultdict(OrderedDict)
    for key, group in grouped_rules:
        rules_by_type[key[0]][key[1]] = list(group)
    rules_by_type = dict(rules_by_type)

    context = {
        'rules_by_type': rules_by_type,
    }
    return render(request, 'index.html', context)
