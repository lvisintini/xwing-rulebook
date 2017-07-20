import fnmatch
import json
import os
import requests
from datetime import datetime
from io import BytesIO
from zipfile import ZipFile

from django.core.management.base import BaseCommand

from integrations.models import Product, DamageDeck, Pilot, Upgrade, Ship, Condition
from integrations.constants import DAMAGE_DECK_TYPES
from integrations.normalizers import normalize


class Command(BaseCommand):
    help = 'Downloads and updates xwing-data content.'

    def handle(self, *args, **options):
        data = {}
        url = requests.get('https://github.com/guidokessels/xwing-data/archive/master.zip')
        zipfile = ZipFile(BytesIO(url.content))
        zip_names = zipfile.namelist()
        for file_path in fnmatch.filter(zip_names, 'xwing-data-master/data/*.*'):
            extracted_file = zipfile.open(file_path)
            file_name = os.path.split(file_path)[1]
            data[file_name.split('.')[0]] = json.loads(extracted_file.read().decode('utf-8'))

        data = normalize(data)

        for d in data[Product.data_key]:
            rd = None
            if 'release_date' in d:
                rd = datetime.strptime(d['release_date'], "%Y-%m-%d").date()
            Product(
                id=d['id'],
                name=d['name'],
                release_date=rd,
                sku=d['sku'],
                data=d,
            ).save()

        for dd_type in DAMAGE_DECK_TYPES.as_list:
            for d in data['damage-deck-{}'.format(dd_type)]:
                try:
                    dd = DamageDeck.objects.get(name=d['name'], type=dd_type)
                except DamageDeck.DoesNotExist:
                    dd = DamageDeck()

                dd.name = d['name']
                dd.type = dd_type
                dd.data = d
                dd.save()

        for model_class in [Pilot, Ship, Upgrade, Condition]:
            for d in data[model_class.data_key]:
                model_class(
                    id=d['id'],
                    name=d['name'],
                    data=d
                ).save()

        for p in Product.objects.all():
            for s in Ship.objects.filter(id__in=[
                ship_data['ship_id']
                for ship_data in p.data.get('contents', {}).get('ships', [])
            ]):
                p.ships.add(s)
            p.save()
