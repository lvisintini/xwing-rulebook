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


class Product(models.Model):
    name = models.CharField(max_length=125)
    sku = models.CharField(max_length=125)
    release_date = models.DateField(blank=True, null=True)
    sources = models.ManyToManyField('rules.Source', blank=True)

    class Meta:
        ordering = ['release_date', 'sku']

    @property
    def json(self):
        if not hasattr(self, '_json'):
            self._json = json.dumps(
                next((p for p in DATA['sources'] if p['id'] == self.id), None),
                indent=2
            )
        return self._json

    def __str__(self):
        return self.name
