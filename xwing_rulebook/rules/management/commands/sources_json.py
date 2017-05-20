import json
from collections import OrderedDict

from django.core.management.base import BaseCommand
from django.db import models

from rules.models import Source


class Command(BaseCommand):
    help = 'Command to print all loaded sources'

    def handle(self, *args, **options):
        sources = []

        qs = Source.objects.all()
        qs = qs.annotate(
            release_date=models.Case(
                models.When(date=None, then=models.Min('products__release_date', distinct=True)),
                default='date'
            )
        )
        qs = qs.order_by('release_date')

        for source in qs:
            s = OrderedDict([
                ('name', source.name),
                ('type', source.type),
                ('code', source.code),
                ('date', source.date.isoformat() if source.date else None),
                ('release_date', source.release_date.isoformat() if source.release_date else None),
                ('sources', list(source.products.values_list('name', flat=True)))
            ])
            sources.append(s)
        self.stdout.write(json.dumps(sources, indent=2, ensure_ascii=False))
