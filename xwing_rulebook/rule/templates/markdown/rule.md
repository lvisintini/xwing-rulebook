{% load markdown %}
## {% if add_anchors %}<a id="p.anchor_id"></a>{% endif %}{{ rule.name }}{% if p.expansion_rule %} †{% endif %}

{% for p in rule.paragraphs.all %}

{% if p.format.type == 'text' %}
{{ p.format.level|indentation}}{% if add_anchors %}<a class="SourceReference" id="{{ p.anchor_id }}">{{ p.reference_text }}</a>{% endif %}{{ p.text }}
{% elif p.format.type == 'item:ul' %}
{{ p.format.level|indentation}}- {% if add_anchors %}<a class="SourceReference" id="{{ p.anchor_id }}">{{ p.reference_text }}</a>{% endif %}{{ p.text }}
{% elif p.format.type == 'item:ol' %}
{{ p.format.level|indentation}}1. {% if add_anchors %}<a class="SourceReference" id="{{ p.anchor_id }}">{{ p.reference_text }}</a>{% endif %}</a>{{ p.text }}
{% endif %}
{% endfor %}
