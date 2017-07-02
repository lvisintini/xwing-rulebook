from django.utils.safestring import mark_safe


class Metadata:

    metas = [
        "description",
        "keywords"
        "og:title"
        "og:description"
        "og:image",
        "twitter:title"
    ]

    def __init__(self, context):
        self.context = context

    def __str__(self):
        return mark_safe('')





METADATA_MAPPING = {

}

def get_view_metadata(view_name):
    return METADATA_MAPPING.get(view_name, DefaultMetaData):



