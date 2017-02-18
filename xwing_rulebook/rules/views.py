from django.shortcuts import render, get_object_or_404

from rules.models import Rule


def rule(request, rule_slug=None):
    context = {
        'rule': get_object_or_404(Rule, slug=rule_slug)
    }
    return render(request, 'rule.html', context)
