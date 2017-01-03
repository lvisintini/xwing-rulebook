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
                      '{source_code} (Page {page})</a>'

    res = template.format(
        indentation='    ' * clause.indentation,
        prefix=PREFIX_TYPE_MAPPING[clause.type],
        anchor='' if not add_anchors else anchor_template.format(
            anchor_id=clause.anchor_id,
            source_code=content.source.code,
            page=content.page,
            clause=clause.id
        ),
        title='' if not content.title else '**{}{}:** '.format(
            content.title, '†' if clause.expansion_related else ''
        ),
        content=content.content,
    )
    return mark_safe(res)

register.filter('format_clause', format_clause)
