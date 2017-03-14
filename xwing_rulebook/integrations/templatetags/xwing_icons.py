import json
import os
import re
from collections import OrderedDict

from django.conf import settings
from django.utils.safestring import mark_safe
from django.template import Library


register = Library()

ICONS = OrderedDict()
ICON_ASSETS_DIR = os.path.join(
    settings.EXTERNAL_ASSETS_DIR, "xwing-data-integration", "icons", "mappings"
)


for dir_path, _, file_names in os.walk(ICON_ASSETS_DIR):
    for f in file_names:
        with open(os.path.abspath(os.path.join(dir_path, f)), 'r') as fo:
            icon_class_mapping = json.load(fo, object_pairs_hook=OrderedDict)
            for key, classes in icon_class_mapping.items():
                ICONS[key] = "<i class=\"{}\"></i>".format(classes)


automata = re.compile(r'\[(' + '|'.join([i.strip('[]') for i in ICONS.keys()]) + r')\]')


@register.filter
def xwing_icons(text):
    result = automata.sub(lambda x: ICONS[x.group()], text)
    return mark_safe(result)
