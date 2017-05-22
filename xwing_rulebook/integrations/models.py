from django.db import models
from django.utils.text import slugify

from integrations.constants import XWING_DATA, DAMAGE_DECK_TYPES


class JSONMixin:
    @property
    def slug(self):
        return slugify(self.json.get('xws', self.name))

    @property
    def json(self):
        if not hasattr(self, '_json'):
            self._json = next((p for p in XWING_DATA[self.data_key] if p['id'] == self.id), None)
        return self._json

    def __str__(self):
        return '[{}] {}'.format(self.slug, self.name)


class Product(models.Model, JSONMixin):
    name = models.CharField(max_length=125)
    sku = models.CharField(max_length=125)
    release_date = models.DateField(blank=True, null=True)
    sources = models.ManyToManyField('rules.Source', blank=True, related_name='products')

    data_key = 'sources'

    class Meta:
        ordering = ['release_date', 'sku']

    @property
    def slug(self):
        return self.sku


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
    def slug(self):
        return slugify(self.type + ' ' + self.name)

    @property
    def json(self):
        if not hasattr(self, '_json'):
            self._json = next(
                (p for p in XWING_DATA[self.data_key] if p['name'] == self.name),
                None
            )
        return self._json

    def __str__(self):
        return '[{}] {}'.format(self.slug, self.name)


class Pilot(JSONMixin, models.Model):
    name = models.CharField(max_length=125)

    data_key = 'pilots'

    @property
    def slug(self):
        return slugify(' '.join([
            self.json['faction'],
            self.json.get('xws', self.name),
        ]))


class Ship(JSONMixin, models.Model):
    name = models.CharField(max_length=125)

    data_key = 'ships'


class Upgrade(JSONMixin, models.Model):
    name = models.CharField(max_length=125)

    data_key = 'upgrades'


class Condition(JSONMixin, models.Model):
    name = models.CharField(max_length=125)

    data_key = 'conditions'

