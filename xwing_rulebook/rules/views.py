from django.shortcuts import render, get_object_or_404

from rules.models import Rule
from rules.helpers import Rule2Markdown


def rule(request, rule_slug=None):
    rule = get_object_or_404(Rule, slug=rule_slug)

    helper = Rule2Markdown(
        rule,
        anchored=True,
        linked=True,
        header_level=1,
    )

    context = {
        'rule': rule,
        'rule2markdown': helper
    }
    return render(request, 'rule.html', context)


def rules_index(request):
    rules = Rule.objects.all()
    context = {
        'rules': rules,
    }
    return render(request, 'index.html', context)
