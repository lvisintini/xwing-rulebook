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
def related_topics(related_topics, rulebook=None, section=None):
    if not related_topics.count():
        return ''

    topics = '**Related Topics:** '


    for SectionRule.objects.filter(rule_id__in=related_topics.value_list('id', flat=True))

    return mark_safe()



**Related Topics:** {% for related_topic in rule.related_topics.all %}{% if not add_anchors %}{{ related_topic }}{% if related_topic.expansion_rule %}†{% endif %}{% else %}<a href="{% if rulebook and section %}{% url 'rule:rule' rulebook_slug=rulebook.slug section_slug=section.slug rule_slug=related_topic.slug %}{% endif %}#{{ related_topic.anchor_id }}">{{ related_topic }}{% if related_topic.expansion_rule %}†{% endif %}</a>{% endif %}{% if not forloop.last %}, {% endif %}{% endfor %}
{% endif %}
