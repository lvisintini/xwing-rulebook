from django.shortcuts import render
from django.http.response import Http404

from rules.models import Rule
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
    rules = Rule.objects.all()
    context = {
        'rules': rules,
    }
    return render(request, 'index.html', context)
