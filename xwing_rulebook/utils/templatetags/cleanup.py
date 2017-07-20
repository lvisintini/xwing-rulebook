import re
from django.template import Library

register = Library()


@register.filter_function
def clean_string(value):
    automata = re.compile(r'\(.*?\)')
    return automata.sub('', value).strip()
