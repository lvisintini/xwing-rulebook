from django.conf import settings
from django.urls import reverse
from django.contrib.staticfiles.templatetags.staticfiles import static


class Metadata:
    metas = [
        "title",
        "description",
        "keywords",
        "charset",
        "author",
        "robots",
        "viewport",
        "og_title",
        "og_description",
        "og_image",
        "msapplication_TileColor",
        "msapplication_TileImage",
        "msapplication_config",
        "theme_color",
        "apple_touch_icon",
        "icon",
        "manifest",
        "mask_icon",
        "shortcut_icon",

    ]

    def __init__(self, context):
        self.context = context

    def __str__(self):
        metas = []
        for m in self.metas:
            data = getattr(self, m)()
            if data:
                metas.append(data)
        return '\n'.join(metas)

# https://dev.twitter.com/cards/types/summary
#<meta name="twitter:card" content="summary" />
#<meta name="twitter:site" content="@flickr" />
#<meta name="twitter:title" content="Small Island Developing States Photo Submission" />
#<meta name="twitter:description" content="View the album on Flickr." />
#<meta name="twitter:image" content="https://farm6.staticflickr.com/5510/14338202952_93595258ff_z.jpg" />
# http://ogp.me/

#og:title - The title of your object as it should appear within the graph, e.g., "The Rock".
#og:type - The type of your object, e.g., "video.movie". Depending on the type you specify, other properties may also be required.
#og:image - An image URL which should represent your object within the graph.
#og:url - The canonical URL of your object that will be used as its permanent ID in the graph, e.g., "http://www.imdb.com/title/tt0117500/".

class DefaultMetaData(Metadata):

    def title(self):
        return "<title>X-Wing Rulebook</title>"

    def description(self):
        return '<meta name="description" content="{}" />'.format(
            "XWing Rulebook is a consolidated set of all the rules for the XWing Miniatures Game."
        )

    def keywords(self):
        return '<meta name="keywords" content="{}" />'.format(','.join([
            'Wing Miniatures Game',
            'XWing Miniatures',
            'XWing',
            'rules',
            'rulebook',
            'complete Rules',
            'consolidated rules',
        ]))

    def charset(self):
        return '<meta charset="utf-8" />'

    def author(self):
        return '<meta name="author" content="Luis Visintini" />'

    def robots(self):
        return '<meta name="robots" content="index, follow" />'

    def viewport(self):
        return '<meta name="viewport" content="width=device-width, initial-scale=1, user-scalable=no" />'

    def og_title(self):
        return '<meta property="og:title" content="XWing Rulebook" />'

    def og_description(self):
        return '<meta property="og:description" content="XWing Rulebook" />'

    def og_image(self):
        return '<meta property="og:image" content="{}" />'.format(static('images/site/logo.svg'))

    def msapplication_TileColor(self):
        return '<meta name="msapplication-TileColor" content="{}" />'.format(settings.BRAND_COLOR)

    def msapplication_TileImage(self):
        return '<meta name="msapplication-TileImage" content="{}" />'.format(static('favicons/mstile-144x144.png'))

    def msapplication_config(self):
        return '<meta name="msapplication-config" content="{}"/ >'.format(reverse('pages:browserconfig.xml'))

    def theme_color(self):
        return '<meta name="theme-color" content="{}" />'.format(settings.BRAND_COLOR)

    def apple_touch_icon(self):
        return '<link rel="apple-touch-icon" sizes="180x180" href="{}" />'.format(
            static('favicons/apple-touch-icon.png')
        )

    def icon(self):
        icons = [
            ('32x32', static('favicons/favicon-32x32.png')),
            ('16x16', static('favicons/favicon-16x16.png')),
        ]
        return '\n'.join([
            '<link rel="icon" type="image/png" sizes="{}" href="{}" />'.format(size, location)
            for size, location  in icons
        ])

    def manifest(self):
        return '<link rel="manifest" href="{}" />'.format(reverse('pages:manifest.json'))

    def mask_icon(self):
        return '<link rel="mask-icon" href="{}" color="{}" />'.format(
            static('favicons/safari-pinned-tab.svg'),
            settings.BRAND_COLOR
        )

    def shortcut_icon(self):
        return '<link rel="shortcut icon" href="{}" />'.format(static('favicons/favicon.ico'))


class RulesIndexMetaData(DefaultMetaData):
    pass


METADATA_MAPPING = {
    #"pages:index": None,
    #"pages:styleguide": None,
    #"pages:resources": None,
    #"pages:contact": None,
    #"pages:wall-of-fame": None,
    #"pages:about": None,
    #"pages:django.contrib.sitemaps.views.sitemap": None,
    #"pages:robots_rule_list": None,
    #"pages:manifest.json": None,
    #"pages:browserconfig.xml": None,
    #"books:book": None,
    #"books:single-page-book": None,
    #"rules:index": None,
    #"rules:rule": None,
    #"faqs:index": None,
}
