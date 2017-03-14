from django.conf import settings
from rules.models import RULE_TYPES


def constants(request):
    return {
        "RULE_TYPES": RULE_TYPES,
    }
