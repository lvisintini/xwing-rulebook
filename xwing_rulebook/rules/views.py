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

    context = {
        'rules': qs.filter(type__in=[RULE_TYPES.RULE, RULE_TYPES.RULE_CLARIFICATION]),
        'pilots': qs.filter(type=RULE_TYPES.CARD, card_type=CARD_TYPES.PILOT),
        'damage_org': qs.filter(type=RULE_TYPES.CARD, card_type=CARD_TYPES.DAMAGE_ORG),
        'damage_tfa': qs.filter(type=RULE_TYPES.CARD, card_type=CARD_TYPES.DAMAGE_TFA),
        'upgrades': qs.filter(type=RULE_TYPES.CARD, card_type=CARD_TYPES.UPGRADE),
        'conditions': qs.filter(type=RULE_TYPES.CARD, card_type=CARD_TYPES.CONDITION),
    }
    return render(request, 'rules_index.html', context)
