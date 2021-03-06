from django.conf import settings as django_settings

from integrations.constants import FACTIONS
from rules.constants import RULE_TYPES, CARD_TYPES, SOURCE_STATUS
from utils.constants import ENVIRONMENTS


def constants(request):
    return {
        "ENVIRONMENTS": ENVIRONMENTS,
        "RULE_TYPES": RULE_TYPES,
        "CARD_TYPES": CARD_TYPES,
        "SOURCE_STATUS": SOURCE_STATUS,
        "FACTIONS": FACTIONS,
    }


def settings(request):
    return {
        "ENVIRONMENT": django_settings.ENVIRONMENT,
        "GOOGLE_TAG_MANAGER_ID": django_settings.GOOGLE_TAG_MANAGER_ID,
    }


def calculated(request):
    return {
        "USE_TRACKING": all([
            django_settings.ENVIRONMENT == ENVIRONMENTS.PRODUCTION,
            bool(django_settings.GOOGLE_TAG_MANAGER_ID),
            not request.user.is_superuser,
            not request.user.is_staff,
        ])
    }