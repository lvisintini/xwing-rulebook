import json
import os
from collections import OrderedDict

from django.conf import settings


DATA_ASSETS_DIR = os.path.join(settings.EXTERNAL_ASSETS_DIR, "xwing-data", "data")
DATA = {}

for dirpath, _, filenames in os.walk(DATA_ASSETS_DIR):
    for f in filenames:
        with open(os.path.abspath(os.path.join(dirpath, f)), 'r') as fo:
            DATA[f.split('.')[0]] = json.load(fo, object_pairs_hook=OrderedDict)


class DAMAGE_DECK_TYPES:
    CORE = 'core'
    CORE_TFA = 'core-tfa'

    as_choices = (
        (CORE, 'Core set'),
        (CORE_TFA, 'The Force Awakens core set'),
    )

    as_list = [
        CORE, CORE_TFA
    ]
