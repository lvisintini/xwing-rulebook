from django.conf import settings as django_settings

from rules.models import RULE_TYPES
from utils.constants import ENVIRONMENTS


def constants(request):
    return {
        "ENVIRONMENTS": ENVIRONMENTS,
        "RULE_TYPES": RULE_TYPES,
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