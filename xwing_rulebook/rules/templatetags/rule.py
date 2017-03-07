from django.conf import settings
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.template import Library
from django.contrib.staticfiles.templatetags.staticfiles import static

from rules.models import CLAUSE_TYPES, RULE_TYPES

register = Library()

PREFIX_TYPE_MAPPING = {
    CLAUSE_TYPES.TEXT: '',
    CLAUSE_TYPES.TABLE: '',
    CLAUSE_TYPES.UNORDERED_ITEM: '- ',
    CLAUSE_TYPES.ORDERED_ITEM: '1. '
}


def format_clause(clause, add_anchors):
    content = clause.current_content

    template = '{indentation}{prefix}{anchor}{title}{content}'
    anchor_template = '<a class="SourceReference" id="{anchor_id}">' \
                      '{source_code}{page}{clause}</a>'

    file = ''
    if content.file:
        file = static(content.file.replace(settings.STATICFILES_DIRS[0], ''))

    res = template.format(
        indentation='    ' * clause.indentation,
        prefix=PREFIX_TYPE_MAPPING[clause.type],
        anchor='' if not add_anchors else anchor_template.format(
            anchor_id=clause.anchor_id,
            source_code=content.source.code,
            page='' if content.page is None else ' (Page {})'.format(content.page),
            clause=' [{}]'.format(clause.id)
        ),
        title='' if not content.title or clause.ignore_title else '**{}{}:** '.format(
            content.title, '†' if clause.expansion_related else ''
        ),
        content=content.content.replace('<FILE>', file),
    )
    return mark_safe(res)

register.filter('format_clause', format_clause)


@register.simple_tag
def related_rules(add_anchor, related_topics, book=None, section=None):
    related_topics = related_topics.filter(type=RULE_TYPES.RULE)

    if not related_topics.count():
        return ''

    topics = '**Related Topics:** {}'
    related = []

    if book:
        related.extend(related_topics.filter(id__in=book.rule_ids))
    else:
        related.extend(related_topics.all())

    if not add_anchor:
        topics = topics.format(', '.join([
            '{}{}'.format(r, '†' if r.expansion_rule else '') for r in related
        ]))
    else:
        topics = topics.format(', '.join([
            '<a href="{}#{}">{}{}</a>'.format(
                reverse(
                    'books:rule',
                    kwargs={
                        'book_slug': book.slug,
                        'section_slug': section.slug,
                        'rule_slug': r.slug
                    }
                ) if book and section else '',
                r.anchor_id,
                r,
                '†' if r.expansion_rule else ''
            )
            for r in related
        ]))

    return mark_safe(topics)
