from django.template import Library
from django.utils.safestring import mark_safe

from pages.metadata import METADATA_MAPPING, DefaultMetaData

register = Library()


@register.simple_tag(takes_context=True)
def metadata(context):
    view_name = context['request'].resolver_match.view_name
    metadata_class = METADATA_MAPPING.get(view_name, DefaultMetaData)
    return mark_safe(str(metadata_class(context)))
