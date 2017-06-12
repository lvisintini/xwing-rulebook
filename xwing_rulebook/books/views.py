from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from django.urls import reverse
from django.http import HttpResponseRedirect

from books.constants import DEFAULT_BOOK_SLUG
from books.models import Book, Section, SectionRule
from markdowns.book import BookRule2Markdown, Book2Markdown


def book(request, book_slug=None, section_slug=None, rule_slug=None):
    if book_slug is None:
        return HttpResponseRedirect(reverse('books:book', args=[
            slug for slug in [DEFAULT_BOOK_SLUG, section_slug, rule_slug] if slug
        ]))

    book = get_object_or_404(Book, slug=book_slug)

    if not section_slug and not rule_slug:
        return render(request, 'book.html', {'book': book})

    elif section_slug and not rule_slug:
        section = Section.objects.filter(slug=section_slug, book=book).first()
        if section:
            return render(request, 'section.html', {'book': book, 'section': section})
        else:
            section_rule = get_object_or_404(
                SectionRule, section__book=book, rule__slug=section_slug
            )

            section = section_rule.section
            rule = section_rule.rule

            helper = BookRule2Markdown(
                book,
                rule,
                anchored=False,
                linked=True,
                anchored_links=False,
                header_level=3,
                url_name='books:book',
                book_slug=book.slug,
                section_slug=section.slug,

            )

            return render(
                request, 'book_rule.html', {
                    'book': book,
                    'section': section,
                    'rule': rule,
                    'bookrule2markdown': helper
                }
            )
    elif not section_slug and rule_slug:
            section_rule = get_object_or_404(
                SectionRule, section__book=book, rule__slug=rule_slug
            )
            section = section_rule.section
            rule = section_rule.rule

            helper = BookRule2Markdown(
                book,
                rule,
                anchored=True,
                linked=True,
                anchored_links=False,
                header_level=3,
                url_name='books:book',
                book_slug=book.slug,
                section_slug=section.slug,

            )
            return render(
                request, 'book_rule.html', {
                    'book': book,
                    'section': section,
                    'rule': rule,
                    'bookrule2markdown': helper
                }
            )
    elif section_slug and rule_slug:
            section_rule = get_object_or_404(
                SectionRule, section__book=book, rule__slug=rule_slug, section__slug=section_slug
            )
            section = section_rule.section
            rule = section_rule.rule

            helper = BookRule2Markdown(
                book,
                rule,
                anchored=True,
                linked=True,
                anchored_links=False,
                header_level=3,
                url_name='books:book',
                book_slug=book.slug,
                section_slug=section.slug,

            )

            return render(
                request, 'book_rule.html', {
                    'book': book,
                    'section': section,
                    'rule': rule,
                    'bookrule2markdown': helper
                }
            )


@user_passes_test(lambda u: u.is_superuser)
def single_page_book(request):
    rulebook = Book.objects.first()
    helper = Book2Markdown(
        rulebook,
        anchored=True,
        linked=False,
        anchored_links=True
    )

    context = {
        'book': rulebook,
        'book2markdown': helper,
    }

    return render(request, 'single_page_book.html', context)
