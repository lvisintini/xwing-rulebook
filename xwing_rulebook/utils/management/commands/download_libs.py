import fnmatch
import os
from io import BytesIO
import requests
from zipfile import ZipFile

from django.conf import settings
from django.core.management.base import BaseCommand

LIBS = [
    {
        "name": "skel",
        "url": "https://github.com/ajlkn/skel/archive/master.zip",
        "mapping": {
            "skel-master/dist/*.scss": "styles",
            "skel-master/dist/*.js": "scripts",
        }
    },
    {
        "name": "xwing-miniatures-font",
        "url": "https://github.com/geordanr/xwing-miniatures-font/archive/master.zip",
        "mapping": {
            "xwing-miniatures-font-master/dist/*.ttf": "fonts",
            "xwing-miniatures-font-master/dist/*.css": "styles",
        }
    }
]


class Command(BaseCommand):
    help = 'Provides complete markdown for a book'

    def handle(self, *args, **options):
        destination_template = os.path.abspath(
            os.path.join(settings.BASE_DIR, 'static/{lib_type}/lib/{lib_name}/')
        )

        for lib in LIBS:
            url = requests.get(lib['url'])
            zipfile = ZipFile(BytesIO(url.content))
            zip_names = zipfile.namelist()

            for pattern, lib_type in lib['mapping'].items():

                for file_path in fnmatch.filter(zip_names, pattern):
                    file_name = os.path.split(file_path)[1]
                    destination = destination_template.format(
                        lib_type=lib_type,
                        lib_name=lib['name']
                    )

                    if not os.path.exists(destination):
                        os.makedirs(destination)

                    extracted_file = zipfile.open(file_path)
                    with open(os.path.join(destination, file_name), 'wb') as f:
                        f.write(extracted_file.read())

                    self.stdout.write(self.style.SUCCESS(
                        "Download OK: {}".format(os.path.join(destination, file_name))
                    ))
