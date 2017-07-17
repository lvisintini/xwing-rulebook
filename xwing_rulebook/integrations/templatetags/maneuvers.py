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
    def __init__(self, speed, maneuver_type, difficulty):
        self.speed = speed
        self.maneuver_type = maneuver_type
        self.difficulty = difficulty

    def __bool__(self):
        return all([
            self.maneuver_type != MANEUVERS_TYPES.NON_EXISTENT,
            self.difficulty != MANEUVERS_DIFFICULTY.UNAVAILABLE,
        ])

    def __repr__(self):
        return '<Maneuver speed="{}" type="{}" difficulty="{}" >'.format(
            self.speed,
            self.maneuver_type,
            self.difficulty,
        )

    @property
    def html_class_name(self):
        types_mapping = OrderedDict([
            (MANEUVERS_TYPES.STATIONARY, 'stationary'),
            (MANEUVERS_TYPES.TURN_LEFT, 'turn-left'),
            (MANEUVERS_TYPES.BANK_LEFT, 'bank-left'),
            (MANEUVERS_TYPES.STRAIGHT, 'straight'),
            (MANEUVERS_TYPES.BANK_RIGHT, 'bank-right'),
            (MANEUVERS_TYPES.TURN_RIGHT, 'turn-right'),
            (MANEUVERS_TYPES.KOIOGRAN_TURN, 'koiogran-turn'),
            (MANEUVERS_TYPES.SEGNORS_LOOP_LEFT, 'segnors-loop-left'),
            (MANEUVERS_TYPES.SEGNORS_LOOP_RIGHT, 'segnors-loop-right'),
            (MANEUVERS_TYPES.TALLON_ROLL_LEFT, 'tallon-roll-left'),
            (MANEUVERS_TYPES.TALLON_ROLL_RIGHT, 'tallon-roll-right'),
            (MANEUVERS_TYPES.REVERSE_BANK_LEFT, 'reverse-bank-left'),
            (MANEUVERS_TYPES.REVERSE_STRAIGHT, 'reverse-straight'),
            (MANEUVERS_TYPES.REVERSE_BANK_RIGHT, 'reverse-bank-right'),
            (MANEUVERS_TYPES.NON_EXISTENT, 'non-existent'),
        ])

        difficulty_mapping = OrderedDict([
            (MANEUVERS_DIFFICULTY.NORMAL, 'normal'),
            (MANEUVERS_DIFFICULTY.EASY, 'easy'),
            (MANEUVERS_DIFFICULTY.DIFFICULT, 'difficult'),
            (MANEUVERS_DIFFICULTY.UNAVAILABLE, 'unavailable'),
        ])

        return 'Maneuver--icon-{}-{}'.format(types_mapping[self.maneuver_type], difficulty_mapping[self.difficulty])


class HugeManeuver(object):
    def __init__(self, speed, maneuver_type, energy):
        self.maneuver_type = maneuver_type
        self.energy = energy
        self.speed = speed

    def __bool__(self):
        return all([
            self.maneuver_type != MANEUVERS_TYPES.NON_EXISTENT,
            self.energy is not None,
        ])

    def __repr__(self):
        return '<HugeManeuver speed="{}" type="{}" energy="{}">'.format(
            self.speed,
            self.maneuver_type,
            self.energy
        )

    @property
    def html_class_name(self):
        types_mapping = OrderedDict([
            (MANEUVERS_TYPES.BANK_LEFT, 'bank-left'),
            (MANEUVERS_TYPES.STRAIGHT, 'straight'),
            (MANEUVERS_TYPES.BANK_RIGHT, 'bank-right'),
            (MANEUVERS_TYPES.NON_EXISTENT, 'non-existent'),
        ])

        energy_mapping = OrderedDict([
            (0, 'e0'),
            (1, 'e1'),
            (2, 'e2'),
            (3, 'e3'),
            (None, 'unavailable')
        ])

        return 'HugeManeuver--icon-{}-{}'.format(types_mapping[self.maneuver_type], energy_mapping[self.energy])


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
            Maneuver(s, maneuver_type, difficulty) if not huge else HugeManeuver(s, maneuver_type, energy if difficulty else None)
            for maneuver_type, difficulty, energy in zip_longest(maneuver_types, maneuvers[s], maneuvers_energy[s])
        ])

    # Additional row and column filtering
    for s in list(reversed(table.keys())):
        if not any(table[s]):
            table.pop(s)
        else:
            break

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
