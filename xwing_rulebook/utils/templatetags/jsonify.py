import json

from django.utils.safestring import mark_safe
from django.core.serializers import serialize
from django.db.models.query import QuerySet
from django.template import Library

register = Library()


def jsonify(object):
    if isinstance(object, QuerySet):
        return serialize('json', object)
    return mark_safe(json.dumps(object))

register.filter('jsonify', jsonify)
