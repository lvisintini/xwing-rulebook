from django.template import Library
from pages.metadata import get_view_metadata

register = Library()


@register.inclusion_tag('includes/_meta.html', takes_context=True)
def address(context):
    view_name = context['request'].resolver_match.view_name

    metadata = get_view_metadata(view_name)(context)

    return {'metadata': metadata}
