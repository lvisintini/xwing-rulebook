{% load rule %}
### {% if add_anchors %}<a id="{{ rule.anchor_id }}"></a>{% endif %}{{ rule.name }}{% if rule.expansion_rule %} †{% endif %}
{% for c in rule.clauses.all %}
{{ c|format_clause:add_anchors }}
{% endfor %}

{% related_rules rule.related_topics rulebook section %}
