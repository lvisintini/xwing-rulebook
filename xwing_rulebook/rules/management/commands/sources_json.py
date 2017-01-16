import json
from collections import OrderedDict

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import models

from rules.models import Source


class Command(BaseCommand):
    help = 'Command to print all loaded sources'

    def handle(self, *args, **options):
        sources = []
        c = 0

        qs = Source.objects.filter(type='RC')
        qs = qs.annotate(
            release_date=models.Case(
                models.When(date=None, then=models.Min('product__release_date', distinct=True)),
                default='date'
            )
        )
        qs = qs.order_by('release_date')

        for source in qs:
            if source.name in ['X-Wing Miniatures Game - Rules Reference', 'X-Wing FAQ']:
                continue
            if '(Corrected)' in source.name:
                continue
            c += 1

            s = OrderedDict([
                ('id', c),
                ('title', source.name.split(" Reference Card")[0]),
                ('subtitle', 'Reference Card' + source.name.split(" Reference Card")[1]),
                ('text', ''),
                (
                    'image',
                    source.file.replace(
                        settings.STATICFILES_DIRS[0], ''
                    ).replace(
                        '/assets', 'images'
                    )
                 ),
                ('sources', list(source.product_set.values_list('id', flat=True)))
            ])

            if source.name == 'Auxiliary Firing Arc':
                s['subtitle'] = ''
            sources.append(s)
        self.stdout.write(json.dumps(sources, indent=2, ensure_ascii=False))
