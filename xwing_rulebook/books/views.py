from django.shortcuts import render, get_object_or_404
from books.models import Book, Section
from rules.models import Rule


def book(request, book_slug, section_slug=None, rule_slug=None):
    context = {
        'book': get_object_or_404(Book, slug=book_slug)
    }

    if not section_slug:
        return render(request, 'book.html', context)

    context['section'] = get_object_or_404(Section, slug=section_slug)

    if not rule_slug:
        return render(request, 'section.html', context)

    context['rule'] = get_object_or_404(Rule, slug=rule_slug)

    return render(request, 'book_rule.html', context)


def single_page_book(request):
    book = Book.objects.first()

    context = {
        'book': book,
    }

    return render(request, 'single_page_book.html', context)