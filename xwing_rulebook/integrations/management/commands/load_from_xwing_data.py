from datetime import datetime
from django.core.management.base import BaseCommand

from integrations.models import Product, DATA


class Command(BaseCommand):
    help = 'Provides complete markdown for a book'

    def handle(self, *args, **options):

        for s in DATA['sources']:
            rd = None
            if 'release_date' in s:
                rd = datetime.strptime(s['release_date'], "%Y-%m-%d").date()
            Product(
                id=s['id'],
                name=s['name'],
                release_date=rd,
                sku=s['sku'],
            ).save()

