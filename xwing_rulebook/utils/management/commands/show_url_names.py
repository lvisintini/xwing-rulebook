from django.core.management.base import BaseCommand
from django.conf import settings

from utils.lib import list_url_names


class Command(BaseCommand):
    help = 'Provides complete markdown for a book'

    def handle(self, *args, **options):
        url_patterns = __import__(settings.ROOT_URLCONF).urlpatterns
        for name in list_url_names(url_patterns):
            self.stdout.write(self.style.SUCCESS(name))
