from django.shortcuts import render, get_object_or_404

from books.models import Book, Section, SectionRule
from books.helpers import Book2Markdown, BookRule2Markdown


def book(request, book_slug, section_slug=None, rule_slug=None):
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
                header_level=1,
                url_name='books:rule',
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
                header_level=1,
                url_name='books:rule',
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
                header_level=1,
                url_name='books:rule',
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


def single_page_book(request):
    rulebook = Book.objects.first()
    helper = Book2Markdown(
        rulebook,
        anchored=True,
        linked=False
    )

    context = {
        'book': rulebook,
        'book2markdown': helper,
    }

    return render(request, 'single_page_book.html', context)
