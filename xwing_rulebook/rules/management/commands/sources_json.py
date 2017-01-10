import json
from collections import OrderedDict

from django.core.management.base import BaseCommand

from rule.models import Source


class Command(BaseCommand):
    help = 'Command to print all loaded sources'

    def handle(self, *args, **options):
        sources = []
        for source in Source.objects.all():
            s = OrderedDict([
                ('name', source.name),
                ('date', source.date.isoformat()),
                ('version', source.version),
                ('code', source.code),
            ])
            sources.append(s)
        self.stdout.write(json.dumps(sources, indent=2, ensure_ascii=False))
