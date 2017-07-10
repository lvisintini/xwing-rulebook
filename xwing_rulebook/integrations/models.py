from django.db import models
from django.utils.text import slugify
from django.contrib.postgres.fields import JSONField

from integrations.constants import DAMAGE_DECK_TYPES


class XWingDataMixin:
    @property
    def slug(self):
        return slugify(self.data.get('xws', self.name))


class Product(models.Model, XWingDataMixin):
    name = models.CharField(max_length=125)
    sku = models.CharField(max_length=125)
    release_date = models.DateField(blank=True, null=True)
    sources = models.ManyToManyField('rules.Source', blank=True, related_name='products')
    data = JSONField(default=dict)

    data_key = 'sources'

    class Meta:
        ordering = ['release_date', 'sku']

    def __str__(self):
        return '[{}] {}'.format(self.slug, self.name)

    @property
    def slug(self):
        return self.sku


class DamageDeck(models.Model):
    name = models.CharField(max_length=125)
    type = models.CharField(
        max_length=25, choices=DAMAGE_DECK_TYPES.as_choices, null=False, blank=False,
        default=DAMAGE_DECK_TYPES.CORE
    )
    data = JSONField(default=dict)

    class Meta:
        unique_together = ('name', 'type')

    @property
    def data_key(self):
        return 'damage-deck-{}'.format(self.type)

    @property
    def slug(self):
        return slugify(self.type + ' ' + self.name)

    def __str__(self):
        return '[{}] {}'.format(self.slug, self.name)


class Pilot(XWingDataMixin, models.Model):
    name = models.CharField(max_length=125)
    data = JSONField(default=dict)

    data_key = 'pilots'

    @property
    def slug(self):
        return slugify(' '.join([
            self.data['faction'],
            self.data.get('xws', self.name),
        ]))

    def __str__(self):
        return '[{}] {}'.format(self.slug, self.name)


class Ship(XWingDataMixin, models.Model):
    name = models.CharField(max_length=125)
    data = JSONField(default=dict)

    data_key = 'ships'

    def __str__(self):
        return '[{}] {}'.format(self.slug, self.name)


class Upgrade(XWingDataMixin, models.Model):
    name = models.CharField(max_length=125)
    data = JSONField(default=dict)

    data_key = 'upgrades'

    def __str__(self):
        return '[{}] {}'.format(self.slug, self.name)


class Condition(XWingDataMixin, models.Model):
    name = models.CharField(max_length=125)
    data = JSONField(default=dict)

    data_key = 'conditions'

    def __str__(self):
        return '[{}] {}'.format(self.slug, self.name)
