import json
import os
import re
from collections import OrderedDict

from django.conf import settings
from django.utils.safestring import mark_safe
from django.template import Library


register = Library()

ICONS = OrderedDict()
ASSETS_DIR = os.path.join(
    settings.EXTERNAL_ASSETS_DIR, "xwing-data-integration", "icons", "mappings"
)


for dirpath, _, filenames in os.walk(ASSETS_DIR):
   for f in filenames:
       with open(os.path.abspath(os.path.join(dirpath, f)), 'r') as fo:
           icon_class_mapping = json.load(fo, object_pairs_hook=OrderedDict)
           for key, classes in icon_class_mapping.items():
               ICONS[key] = "<i class=\"{}\"></i>".format(classes)


automata = re.compile(r'\[(' + '|'.join([i.strip('[]') for i in ICONS.keys()]) + r')\]')

def xwing_icons(text):
    result = automata.sub(lambda x: ICONS[x.group()], text)
    return mark_safe(result)

register.filter('xwing_icons', xwing_icons)
