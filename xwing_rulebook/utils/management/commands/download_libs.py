import fnmatch
import os
import requests
import shutil
from io import BytesIO
from zipfile import ZipFile

from django.conf import settings
from django.core.management.base import BaseCommand

from utils.lib import find_common_root_path


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
    },
    {
        "name": "font-awesome",
        "url": "https://github.com/FortAwesome/Font-Awesome/archive/master.zip",
        "mapping": {
            "Font-Awesome-master/fonts/*.*": "fonts",
            "Font-Awesome-master/scss/*.*": "styles",
        }
    },
    {
        "name": "normalize.css",
        "url": "https://github.com/necolas/normalize.css/archive/master.zip",
        "mapping": {
            "normalize.css-master/normalize.css": "styles",
        }
    },
    {
        "name": "xwing-data",
        "url": "https://github.com/guidokessels/xwing-data/archive/master.zip",
        "mapping": {
            "xwing-data-master/images/*.*": "images",
        },
        "normalize": True,
    },
]


class Command(BaseCommand):
    help = 'Provides complete markdown for a book'

    @staticmethod
    def normalize_path(path):
        path = path.lower()
        path = path.replace(' ', '-')
        return path

    def handle(self, *args, **options):
        destination_template = os.path.abspath(
            os.path.join(settings.BASE_DIR, 'static/{lib_type}/lib/{lib_name}/')
        )

        for lib in LIBS:
            url = requests.get(lib['url'])
            zipfile = ZipFile(BytesIO(url.content))
            zip_names = zipfile.namelist()

            for pattern, lib_type in lib['mapping'].items():
                destination = destination_template.format(
                    lib_type=lib_type,
                    lib_name=lib['name']
                )
                if not os.path.exists(destination):
                    os.makedirs(destination)
                else:
                    shutil.rmtree(destination)
                    os.makedirs(destination)

                common_root = find_common_root_path(
                    '/'.join(pattern.split('/')[:-1]),
                    *fnmatch.filter(zip_names, pattern)
                )

                for file_path in fnmatch.filter(zip_names, pattern):
                    zip_path, file_name = os.path.split(file_path)
                    relative_path = zip_path.replace(common_root, '')

                    if not file_name:
                        # This means a directory was matched and we will ignore it.
                        continue

                    extracted_file = zipfile.open(file_path)

                    final_folder_path = destination + relative_path
                    if lib.get('normalize'):
                        final_folder_path = self.normalize_path(final_folder_path)

                    if not os.path.exists(final_folder_path):
                        os.makedirs(final_folder_path)

                    final_file_path = os.path.join(final_folder_path, file_name)
                    if lib.get('normalize'):
                        final_file_path = self.normalize_path(final_file_path)

                    with open(final_file_path, 'wb') as f:
                        f.write(extracted_file.read())

                    self.stdout.write(self.style.SUCCESS(
                        "Download OK: {}".format(final_file_path)
                    ))
