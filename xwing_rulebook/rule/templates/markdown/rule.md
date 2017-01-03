{% load markdown %}
### {% if add_anchors %}<a id="{{ rule.anchor_id }}"></a>{% endif %}{{ rule.name }}{% if rule.expansion_rule %} †{% endif %}
{% for c in rule.clauses.all %}
{{ c|format_clause:add_anchors }}
{% endfor %}
{% if rule.related_topics.count %}
**Related Topics:** {% for related_topic in rule.related_topics.all %}{% if not add_anchors %}{{ related_topic }}{% if related_topic.expansion_rule %}†{% endif %}{% else %}<a href="#{{ related_topic.anchor_id }}">{{ related_topic }}{% if related_topic.expansion_rule %}†{% endif %}</a>{% endif %}{% if not forloop.last %}, {% endif %}{% endfor %}
{% endif %}