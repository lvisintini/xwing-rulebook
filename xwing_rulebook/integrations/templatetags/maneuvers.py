from itertools import zip_longest

from django.utils.safestring import mark_safe
from django.template import Library

from integrations.constants import MANEUVERS_TYPES, MANEUVERS_DIFFICULTY
from integrations.models import Pilot

register = Library()


class Maneuver(object):
    def __init__(self, maneuver_type, difficulty, energy=None):
        self.maneuver_type = maneuver_type
        self.difficulty = difficulty
        self.energy = energy

    def __bool__(self):
        return bool(self.difficulty)

    def __str__(self):
        pass

    def __repr__(self):
        return '<Maneuver type="{}" difficulty"{}" energy="{}">'.format(
            self.maneuver_type[1:-1],
            self.difficulty,
            self.energy
        )


def process_maneuvers_data(maneuvers, maneuvers_energy=None):
    # assume array lengths have been normalized

    table = []
    huge = False

    if maneuvers_energy is not None:
        huge = True
        maneuvers_energy = [[]] * len(maneuvers)

    speed_zero = True and not huge
    for s in range(len(maneuvers)):

        if speed_zero:
            speed_zero = False
            maneuver_types = MANEUVERS_TYPES.speed_zero
        else:
            maneuver_types = MANEUVERS_TYPES.small_and_large if not huge else MANEUVERS_TYPES.huge

        table.append([
            Maneuver(maneuver_type, difficulty, energy)
            for maneuver_type, difficulty, energy in zip_longest(maneuver_types, maneuvers[s], maneuvers_energy[s])
        ])

    # Additional row and column filtering

    return table


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
