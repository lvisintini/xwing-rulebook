from django.urls import reverse
from django.utils.safestring import mark_safe
from django.template import Library

from rule.models import ClauseContentVersion

register = Library()

PREFIX_TYPE_MAPPING = {
    'text': '',
    'table': '',
    'image': '',
    'item:ul': '- ',
    'item:ol': '1. '
}


def format_clause(clause, add_anchors):
    content = ClauseContentVersion.objects.get(
        clause=clause,
        active=True
    ).content

    template = '{indentation}{prefix}{anchor}{title}{content}'
    anchor_template = '<a class="SourceReference" id="{anchor_id}">' \
                      '{source_code}{page}{clause}</a>'

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
        content=content.content,
    )
    return mark_safe(res)

register.filter('format_clause', format_clause)


@register.simple_tag
def related_rules(add_anchor, related_topics, rulebook=None, section=None):
    if not related_topics.count():
        return ''

    topics = '**Related Topics:** {}'
    related = []

    if rulebook:
        related.extend(related_topics.filter(id__in=rulebook.rule_ids))
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
                    'rule:rule',
                    kwargs={
                        'rulebook_slug': rulebook.slug,
                        'section_slug': section.slug,
                        'rule_slug': r.slug
                    }
                ) if rulebook and section else '',
                r.anchor_id,
                r,
                '†' if r.expansion_rule else ''
            )
            for r in related
        ]))

    return mark_safe(topics)
