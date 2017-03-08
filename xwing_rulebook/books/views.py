from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect

from books.models import Book, Section, SectionRule
from rules.models import Rule


def book(request, book_slug, section_slug=None, rule_slug=None):
    context = {
        'book': get_object_or_404(Book, slug=book_slug)
    }

    if not section_slug:
        return render(request, 'book.html', context)

    context['section'] = Section.objects.filter(slug=section_slug, book=context['book']).first()

    if not rule_slug:
        if context['section'] is not None:
            return render(request, 'section.html', context)

        # If the section was not found, try to use section_slug as a rule_slug and find the section.
        # The redirect to the book:rule url.
        rule_slug = section_slug
        try:
            section_slug = SectionRule.objects.select_related('section').get(
                section__book=book,
                rule__slug=rule_slug,
            ).section.slug
        except SectionRule.DoesNotExist:
            raise Http404
        else:
            redirect(
                'boos:rule', book_slug=book.slug, section_slug=section_slug, rule_slug=rule_slug
            )

    context['rule'] = get_object_or_404(Rule, slug=rule_slug)

    return render(request, 'book_rule.html', context)


def single_page_book(request):
    book = Book.objects.first()

    context = {
        'book': book,
    }

    return render(request, 'single_page_book.html', context)