from django.conf import settings
from django.urls import reverse
from django.contrib.staticfiles.templatetags.staticfiles import static
from utils.lib import site_url_from_request


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
        "og_url",

        "twitter_card",
        "twitter_site",
        "twitter_creator",
        "twitter_title",
        "twitter_description",
        "twitter_image",

        "msapplication_TileColor",
        "msapplication_TileImage",
        "msapplication_config",
        "theme_color",
        "apple_touch_icon",
        "icon",
        "manifest",
        "mask_icon",
        "shortcut_icon",

        "canonical",
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


class DefaultMetaData(Metadata):
    default_title = "X-Wing Rulebook"
    default_description = 'XWing Rulebook is a consolidated set of all the rules for the XWing Miniatures Game.'
    default_keywords = [
        'Wing Miniatures Game',
        'XWing Miniatures',
        'XWing',
        'rules',
        'rulebook',
        'complete rules',
        'consolidated rules',
    ]
    default_og_type = "website"
    default_twitter_handle = None

    def title(self):
        return "<title>{}</title>".format(self.default_title)

    def description(self):
        return '<meta name="description" content="{}" />'.format(self.default_description)

    def keywords(self):
        return '<meta name="keywords" content="{}" />'.format(','.join(self.default_keywords))

    def charset(self):
        return '<meta charset="utf-8" />'

    def author(self):
        return '<meta name="author" content="Luis Visintini" />'

    def robots(self):
        return '<meta name="robots" content="index, follow" />'

    def viewport(self):
        return '<meta name="viewport" content="width=device-width, initial-scale=1, user-scalable=no" />'

    def og_title(self):
        return '<meta property="og:title" content="{}" />'.format(self.default_title)

    def og_description(self):
        return '<meta property="og:description" content="{}" />'.format(self.default_description)

    def og_type(self):
        return '<meta property="og:type" content="{}" />'.format(self.default_og_type)

    def og_image(self):
        return '\n'.join([
            '<meta property="og:image" content="{image_url}" />',
            '<meta property="og:image:secure_url" content="{image_url}" />',
            '<meta property="og:image:type" content="{type}" />',
            '<meta property="og:image:width" content="{width}" />',
            '<meta property="og:image:height" content="{height}" />',
        ]).format(
            image_url=site_url_from_request(self.context['request']) + static('images/site/logo-200x200.png'),
            type='image/png',
            width='200',
            height='200',
        )

    def og_url(self):
        return '<meta property="og:url" content="{}" />'.format(
            site_url_from_request(self.context['request']) + self.context['request'].path
        )

    def twitter_card(self):
        return '<meta name="twitter:card" content="summary" />'

    def twitter_site(self):
        if self.default_twitter_handle:
            return '<meta name="twitter:site" content="{}" />'.format(self.default_twitter_handle)
        return

    def twitter_creator(self):
        return '<meta name="twitter:creator" content="@lvisintini" />'

    def twitter_title(self):
        return '<meta name="twitter:title" content="{}" />'.format(self.default_title)

    def twitter_description(self):
        return '<meta name="twitter:description" content="{}" />'.format(self.default_description)

    def twitter_image(self):
        return '<meta name="twitter:image" content="{}" />'.format(
            site_url_from_request(self.context['request']) + static('images/site/logo-200x200.png')
        )

    def msapplication_TileColor(self):
        return '<meta name="msapplication-TileColor" content="{}" />'.format(settings.BRAND_COLOR)

    def msapplication_TileImage(self):
        return '<meta name="msapplication-TileImage" content="{}" />'.format(
            site_url_from_request(self.context['request']) + static('favicons/mstile-144x144.png')
        )

    def msapplication_config(self):
        return '<meta name="msapplication-config" content="{}"/ >'.format(
            site_url_from_request(self.context['request']) + reverse('pages:browserconfig.xml')
        )

    def theme_color(self):
        return '<meta name="theme-color" content="{}" />'.format(settings.BRAND_COLOR)

    def apple_touch_icon(self):
        return '<link rel="apple-touch-icon" sizes="180x180" href="{}" />'.format(
            site_url_from_request(self.context['request']) + static('favicons/apple-touch-icon.png')
        )

    def icon(self):
        icons = [
            ('32x32', site_url_from_request(self.context['request']) + static('favicons/favicon-32x32.png')),
            ('16x16', site_url_from_request(self.context['request']) + static('favicons/favicon-16x16.png')),
        ]
        return '\n'.join([
            '<link rel="icon" type="image/png" sizes="{}" href="{}" />'.format(size, location)
            for size, location in icons
        ])

    def manifest(self):
        return '<link rel="manifest" href="{}" />'.format(
            site_url_from_request(self.context['request']) + reverse('pages:manifest.json')
        )

    def mask_icon(self):
        return '<link rel="mask-icon" href="{}" color="{}" />'.format(
            site_url_from_request(self.context['request']) + static('favicons/safari-pinned-tab.svg'),
            settings.BRAND_COLOR
        )

    def shortcut_icon(self):
        return '<link rel="shortcut icon" href="{}" />'.format(
            site_url_from_request(self.context['request']) + static('favicons/favicon.ico')
        )

    def canonical(self):
        return '<link rel="canonical" href="{}" />'.format(
            site_url_from_request(self.context['request']) + self.context['request'].path
        )


class RulesIndexMetaData(DefaultMetaData):
    pass


METADATA_MAPPING = {
    "pages:index": DefaultMetaData,
    #"pages:styleguide": None,
    #"pages:resources": None,
    #"pages:contact": None,
    #"pages:wall-of-fame": None,
    #"pages:about": None,
    #"pages:django.contrib.sitemaps.views.sitemap": None,
    #"pages:robots_rule_list": None,
    #"books:book": None,
    #"rules:index": None,
    #"rules:rule": None,
    #"faqs:index": None,
}
