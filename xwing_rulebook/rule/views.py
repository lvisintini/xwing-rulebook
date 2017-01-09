from django.shortcuts import render, get_object_or_404
from .models import RuleBook, BookSection, Rule


def rulebook(request, rulebook_slug, section_slug=None, rule_slug=None):
    context = {
        'rulebook': get_object_or_404(RuleBook, slug=rulebook_slug)
    }

    if not section_slug:
        return render(request, 'html/rulebook.html', context)

    context['section'] = get_object_or_404(BookSection, slug=section_slug)

    if not rule_slug:
        return render(request, 'html/booksection.html', context)

    context['rule'] = get_object_or_404(Rule, slug=rule_slug)

    return render(request, 'html/rule.html', context)


def single_page_rulebook(request):
    rb = RuleBook.objects.first()

    context = {
        'rb': rb,
    }

    return render(request, 'html/single_page_rulebook.html', context)
