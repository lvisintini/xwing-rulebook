from collections import OrderedDict
import json
import os

from django.conf import settings
from django.db import models


DATA_ASSETS_DIR = os.path.join(settings.EXTERNAL_ASSETS_DIR, "xwing-data", "data")
DATA = {}
for dirpath, _, filenames in os.walk(DATA_ASSETS_DIR):
    for f in filenames:
        with open(os.path.abspath(os.path.join(dirpath, f)), 'r') as fo:
            DATA[f.split('.')[0]] = json.load(fo, object_pairs_hook=OrderedDict)


class DAMAGE_DECK_TYPES:
    CORE = 'core'
    CORE_TFA = 'core-tfa'

    as_choices = (
        (CORE, 'Core set'),
        (CORE_TFA, 'The Force Awakens core set'),
    )

    as_list = [
        CORE, CORE_TFA
    ]


class JSONMixin:

    @property
    def json(self):
        if not hasattr(self, '_json'):
            self._json = json.dumps(
                next((p for p in DATA[self.data_key] if p['id'] == self.id), None),
                indent=2
            )
        return self._json


class Product(models.Model, JSONMixin):
    name = models.CharField(max_length=125)
    sku = models.CharField(max_length=125)
    release_date = models.DateField(blank=True, null=True)
    sources = models.ManyToManyField('rules.Source', blank=True)

    data_key = 'sources'

    class Meta:
        ordering = ['release_date', 'sku']

    def __str__(self):
        return self.name


class DamageDeck(models.Model):
    name = models.CharField(max_length=125)
    type = models.CharField(
        max_length=25, choices=DAMAGE_DECK_TYPES.as_choices, null=False, blank=False,
        default=DAMAGE_DECK_TYPES.CORE
    )

    class Meta:
        unique_together = ('name', 'type')

    @property
    def data_key(self):
        return 'damage-deck-{}'.format(self.type)

    @property
    def json(self):
        if not hasattr(self, '_json'):
            self._json = json.dumps(
                next((p for p in DATA[self.data_key] if p['name'] == self.name), None),
                indent=2
            )
        return self._json


    def __str__(self):
        return self.name


class Pilot(models.Model, JSONMixin):
    name = models.CharField(max_length=125)

    data_key = 'pilots'

    def __str__(self):
        return self.name


class Ship(models.Model, JSONMixin):
    name = models.CharField(max_length=125)

    data_key = 'ships'

    def __str__(self):
        return self.name


class Upgrade(models.Model, JSONMixin):
    name = models.CharField(max_length=125)

    data_key = 'upgrades'

    def __str__(self):
        return self.name
