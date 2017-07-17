from django.db import models
from django.utils.text import slugify
from django.contrib.postgres.fields import JSONField
from django.contrib.postgres.fields.jsonb import KeyTransform, KeyTextTransform
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.utils.functional import cached_property
from integrations.constants import DAMAGE_DECK_TYPES, SHIP_SIZES


class Product(models.Model):
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

    @property
    def thumb_static_url(self):
        return static('images/lib/xwing-data/' + self.data['thumb']) if 'thumb' in self.data else None

    @property
    def image_static_url(self):
        return static('images/lib/xwing-data/' + self.data['image']) if 'image' in self.data else None


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
        return slugify(' '.join([
            'damage-deck',
            self.type,
            self.name,
        ]))

    def __str__(self):
        return '[{}] {}'.format(self.slug, self.name)

    @property
    def image_static_url(self):
        return static('images/lib/xwing-data/' + self.data['image']) if 'image' in self.data else None


class ShipManager(models.Manager):
    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.annotate(size=KeyTextTransform('size', 'data'))

        qs = qs.annotate(
            size_order=models.Case(
                *[
                    models.When(
                        size=s,
                        then=SHIP_SIZES.as_list.index(s)
                    )
                    for s in SHIP_SIZES.as_list
                ],
                default=100,
                output_field=models.IntegerField()
            )
        )

        return qs


class Ship(models.Model):
    name = models.CharField(max_length=125)
    data = JSONField(default=dict)

    data_key = 'ships'

    objects = ShipManager()

    def __str__(self):
        return '[{}] {}'.format(self.slug, self.name)

    @property
    def slug(self):
        return slugify(self.name)

    @cached_property
    def factions(self):
        return self.data.get('factions', [])


class PilotManager(models.Manager):
    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.annotate(ship_id=KeyTransform("ship' -> 'ship_id", 'data'))
        qs = qs.annotate(ship_name=KeyTransform("ship' ->> 'name", 'data'))
        return qs


class Pilot(models.Model):
    name = models.CharField(max_length=125)
    data = JSONField(default=dict)

    data_key = 'pilots'

    objects = PilotManager()

    @property
    def slug(self):
        return slugify(' '.join([
            'pilot',
            self.data['faction'],
            self.data.get('xws', self.name),
        ]))

    @property
    def image_static_url(self):
        return static('images/lib/xwing-data/' + self.data['image']) if 'image' in self.data else None

    def __str__(self):
        return '[{}] {}'.format(self.slug, self.name)

    @cached_property
    def ship(self):
        return Ship.objects.get(id=self.ship_id) if self.ship_id is not None else None


class Upgrade(models.Model):
    name = models.CharField(max_length=125)
    data = JSONField(default=dict)

    data_key = 'upgrades'

    def __str__(self):
        return '[{}] {}'.format(self.slug, self.name)

    @property
    def slug(self):
        return slugify(' '.join([
            'upgrade',
            self.data.get('xws', self.name),
        ]))

    @property
    def image_static_url(self):
        return static('images/lib/xwing-data/' + self.data['image']) if 'image' in self.data else None


class Condition(models.Model):
    name = models.CharField(max_length=125)
    data = JSONField(default=dict)

    data_key = 'conditions'

    def __str__(self):
        return '[{}] {}'.format(self.slug, self.name)

    @property
    def image_static_url(self):
        return static('images/lib/xwing-data/' + self.data['image']) if 'image' in self.data else None

    @property
    def slug(self):
        return slugify(' '.join([
            'condition',
            self.data.get('xws', self.name),
        ]))
