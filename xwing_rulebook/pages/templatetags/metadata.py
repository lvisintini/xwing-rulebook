from django.template import Library

from pages.metadata import METADATA_MAPPING, DefaultMetaData

register = Library()


@register.inclusion_tag('includes/_meta.html', takes_context=True)
def metadata(context):
    view_name = context['request'].resolver_match.view_name
    metadata_class = METADATA_MAPPING.get(view_name, DefaultMetaData)
    return {'metadata': metadata_class(context)}
