from django.shortcuts import render, get_object_or_404

from books.models import Book, Section, SectionRule


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
            return render(
                request, 'book_rule.html', {'book': book, 'section': section, 'rule': rule}
            )
    elif not section_slug and rule_slug:
            section_rule = get_object_or_404(
                SectionRule, section__book=book, rule__slug=rule_slug
            )
            section = section_rule.section
            rule = section_rule.rule
            return render(
                request, 'book_rule.html', {'book': book, 'section': section, 'rule': rule}
            )
    elif section_slug and rule_slug:
            section_rule = get_object_or_404(
                SectionRule, section__book=book, rule__slug=rule_slug, section__slug=section_slug
            )
            section = section_rule.section
            rule = section_rule.rule
            return render(
                request, 'book_rule.html', {'book': book, 'section': section, 'rule': rule}
            )


def single_page_book(request):
    book = Book.objects.first()

    context = {
        'book': book,
    }

    return render(request, 'single_page_book.html', context)