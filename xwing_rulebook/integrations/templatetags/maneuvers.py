from django.utils.safestring import mark_safe
from django.template import Library

from integrations.constants import MANEUVERS, MANEUVERS_DIFFICULTY
from integrations.models import Pilot

register = Library()


def process_maneuvers_data(maneuvers, maneuvers_energy=None):
    return ''


@register.filter
def maneuvers_html(model):
    if isinstance(model, Pilot):
        pass
    return mark_safe('')


@register.filter
def maneuvers_markdown(model):
    if isinstance(model, Pilot):
        pass
    return mark_safe('')
