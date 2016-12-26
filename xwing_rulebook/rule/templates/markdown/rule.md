{% load markdown %}
## {{ rule.name }}{% if p.expansion_rule %} †{% endif %}

{% for p in rule.paragraphs.all %}
{% if p.format.type == 'text' %}
{{ p.format.level|indentation}}{{ p.text }}
{% elif p.format.type == 'item:ol' %}
{{ p.format.level|indentation}}- {{ p.text }}
{% elif p.format.type == 'item:ul' %}
{{ p.format.level|indentation}}1. {{ p.text }}
{% endif %}
{% endfor %}
