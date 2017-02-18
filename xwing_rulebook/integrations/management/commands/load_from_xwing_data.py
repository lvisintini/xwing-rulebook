from datetime import datetime
from django.core.management.base import BaseCommand

from integrations.models import Product, DamageDeck, Pilot, Upgrade, Ship, DATA, DAMAGE_DECK_TYPES


class Command(BaseCommand):
    help = 'Provides complete markdown for a book'

    def handle(self, *args, **options):

        for d in DATA[Product.data_key]:
            rd = None
            if 'release_date' in d:
                rd = datetime.strptime(d['release_date'], "%Y-%m-%d").date()
            Product(
                id=d['id'],
                name=d['name'],
                release_date=rd,
                sku=d['sku'],
            ).save()

        for dd_type in DAMAGE_DECK_TYPES.as_list:
            for d in DATA['damage-deck-{}'.format(dd_type)]:
                try:
                    dd = DamageDeck.objects.get(name=d['name'], type=dd_type)
                except DamageDeck.DoesNotExist:
                    dd = DamageDeck()

                dd.name = d['name']
                dd.type = dd_type
                dd.save()

        for model_class in [Pilot, Ship, Upgrade]:
            for d in DATA[model_class.data_key]:
                model_class(
                    id=d['id'],
                    name=d['name'],
                ).save()
