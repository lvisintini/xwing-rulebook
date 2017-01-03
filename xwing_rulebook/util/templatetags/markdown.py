from django.utils.safestring import mark_safe
from django.template import Library

from markdown2 import Markdown

register = Library()

PREFIX_TYPE_MAPPING = {
    'text': '',
    'table': '',
    'image': '',
    'item:ul': '- ',
    'item:ol': '1. '
}


def md2html(subject):
    markdown = Markdown(extras=["tables"])

    if hasattr(subject, 'to_markdown'):
        subject = subject.to_markdown()

    return mark_safe(markdown.convert(subject))

register.filter('md2html', md2html)


def format_clause(clause, add_anchors):
    content = clause.clause_content

    template = '{indentation}{prefix}{anchor}{title}{content}'
    anchor_template = '<a class="SourceReference" id="{anchor_id}">{source_code} (Page {page})</a>'

    res = template.format(
        indentation='    ' * clause.indentation,
        prefix=PREFIX_TYPE_MAPPING[clause.type],
        anchor='' if not add_anchors else anchor_template.format(
            anchor_id=clause.anchor_id,
            source_code=content.source.code,
            page=content.page,
        ),
        title='' if not content.title else '**{}{}:** '.format(
            content.title, '†' if clause.expansion_related else ''
        ),
        content=content.content,
    )
    return mark_safe(res)

register.filter('format_clause', format_clause)
