from collections import OrderedDict
from itertools import zip_longest

from django.utils.safestring import mark_safe
from django.template import Library

from integrations.constants import MANEUVERS_TYPES, MANEUVERS_DIFFICULTY
from integrations.models import Ship, Pilot
from integrations.templatetags.xwing_icons import xwing_icons
from utils.lib import render_template


register = Library()


class Maneuver(object):
    def __init__(self, speed, maneuver_type, difficulty, energy=None):
        self.maneuver_type = maneuver_type
        self.difficulty = difficulty
        self.energy = energy
        self.speed = speed

    def __bool__(self):
        return all([
            self.maneuver_type != MANEUVERS_TYPES.NON_EXISTANT,
            self.difficulty != MANEUVERS_DIFFICULTY.UNAVAILABLE,
        ])

    def __str__(self):
        if not self:
            return ''
        return mark_safe(self.maneuver_type)

    def energy_tokens(self):
        return mark_safe('[Energy]' * self.energy if self.energy is not None else '')

    def __repr__(self):
        return '<Maneuver speed="{}" type="{}" difficulty="{}" energy="{}">'.format(
            self.speed,
            self.maneuver_type,
            self.difficulty,
            self.energy
        )

    @property
    def difficulty_class(self):
        return MANEUVERS_DIFFICULTY.as_classes.get(self.difficulty, '')


def process_maneuvers_data(maneuvers, maneuvers_energy=None):
    # assume array lengths have been normalized

    table = OrderedDict([(x, [])for x in range(len(maneuvers))])

    huge = False
    if maneuvers_energy is not None:
        huge = True
    else:
        maneuvers_energy = [[]] * len(maneuvers)

    speed_zero = True and not huge
    for s in range(len(maneuvers)):

        if speed_zero:
            speed_zero = False
            maneuver_types = MANEUVERS_TYPES.speed_zero
        else:
            maneuver_types = MANEUVERS_TYPES.small_and_large if not huge else MANEUVERS_TYPES.huge

        table[s].extend([
            Maneuver(s, maneuver_type, difficulty, energy)
            for maneuver_type, difficulty, energy in zip_longest(maneuver_types, maneuvers[s], maneuvers_energy[s])
        ])

    # Additional row and column filtering
    for s in list(reversed(table.keys())):
        if not any(table[s]):
            table.pop(s)

    if 0 in table and not any(table[0]):
        table.pop(0)

    columns_to_clear = []
    for column in range(5, len(MANEUVERS_TYPES.small_and_large if not huge else MANEUVERS_TYPES.huge)):
        if not any([table[s][column] for s in table.keys()]):
            columns_to_clear.insert(0, column)

    for s in table.keys():
        for c in columns_to_clear:
            table[s].pop(c)

    return table


@register.filter
def maneuvers_html(model):
    maneuvers = None
    maneuvers_energy = None

    if isinstance(model, Pilot):
        maneuvers = model.data.get('ship_override', {}).get(
            'maneuvers', model.ship.data.get('maneuvers')
        )
        maneuvers_energy = model.data.get('ship_override', {}).get(
            'maneuvers_energy', model.ship.data.get('maneuvers_energy')
        )
    elif isinstance(model, Ship):
        maneuvers = model.data.get('maneuvers')
        maneuvers_energy = model.data.get('maneuvers_energy')

    if maneuvers is None:
        return ''

    data = process_maneuvers_data(maneuvers, maneuvers_energy)

    return mark_safe(xwing_icons(render_template('integrations/maneuvers_table.html', {'maneuvers': data})))
