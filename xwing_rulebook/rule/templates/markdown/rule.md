{% load markdown %}
## {% if add_anchors %}<a id="{{ rule.anchor_id }}"></a>{% endif %}{{ rule.name }}{% if rule.expansion_rule %} †{% endif %}
{% for p in rule.paragraphs.all %}
{% if p.format.type == 'text' %}{{ p.format.level|indentation}}{% if add_anchors %}<a class="SourceReference" id="{{ p.anchor_id }}">{{ p.reference_text }}</a>{% endif %}{{ p | format_paragraph }}
{% elif p.format.type == 'item:ul' %}{{ p.format.level|indentation}}- {% if add_anchors %}<a class="SourceReference" id="{{ p.anchor_id }}">{{ p.reference_text }}</a>{% endif %}{{ p | format_paragraph }}
{% elif p.format.type == 'item:ol' %}{{ p.format.level|indentation}}1. {% if add_anchors %}<a class="SourceReference" id="{{ p.anchor_id }}">{{ p.reference_text }}</a>{% endif %}{{ p | format_paragraph }}
{% elif p.format.type == 'table' %}{% if add_anchors %}<a class="SourceReference" id="{{ p.anchor_id }}">{{ p.reference_text }}</a>{% endif %}{{ p.text }}
{% endif %}{% endfor %}
{% if rule.related_topics.count %}
**Related Topics:** {% for related_topic in rule.related_topics.all %}{% if not add_anchors %}{{ related_topic }}{% if related_topic.expansion_rule %}†{% endif %}{% else %}<a href="#{{ related_topic.anchor_id }}">{{ related_topic }}{% if related_topic.expansion_rule %}†{% endif %}</a>{% endif %}{% if not forloop.last %}, {% endif %}{% endfor %}
{% endif %}