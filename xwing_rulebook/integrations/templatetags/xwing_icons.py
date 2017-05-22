import re

from django.utils.safestring import mark_safe
from django.template import Library

from integrations.icons import ICONS

register = Library()

@register.filter
def xwing_icons(text):
    automata = re.compile(r'\[(' + '|'.join([i.strip('[]') for i in ICONS.keys()]) + r')\]')
    result = automata.sub(lambda x: "<i class=\"{}\"></i>".format(ICONS[x.group()]), text)
    return mark_safe(result)
