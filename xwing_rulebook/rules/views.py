from django.shortcuts import render, get_object_or_404

from rules.models import Rule


def rule(request, rule_slug=None):
    r = get_object_or_404(Rule, slug=rule_slug)
    context = {
        'rule': r,
    }
    return render(request, 'rule.html', context)


def rules_index(request):
    rules = Rule.objects.all()
    context = {
        'rules': rules,
    }
    return render(request, 'index.html', context)
