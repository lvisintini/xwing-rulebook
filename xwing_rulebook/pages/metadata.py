from django.conf import settings
from django.urls import reverse
from django.contrib.staticfiles.templatetags.staticfiles import static

from rules.constants import CLAUSE_GROUPS, RULE_TYPES, CARD_TYPES
from utils.lib import site_url_from_request


class Metadata:
    separator = ' | '

    def __init__(self, context):
        self.context = context

    def absolute_url(self, relative_url):
        return site_url_from_request(self.context['request']) + relative_url


class DefaultMetaData(Metadata):
    default_title = ["X-Wing Rulebook", ]
    default_description = 'A consolidated and complete list of all the rules for the XWing Miniatures Game.'
    default_keywords = [
        'X-Wing Miniatures Game',
        'X-Wing Miniatures',
        'X-Wing',
        'XWing',
        'rules',
        'rulebook',
        'complete rules',
        'consolidated rules',
    ]
    default_og_type = "website"
    default_site_twitter_handle = None

    def title(self):
        return self.default_title[0]

    def description(self):
        return self.default_description

    def keywords(self):
        return ','.join(self.default_keywords)

    def charset(self):
        return "utf-8"

    def author(self):
        return "Luis Visintini"

    def robots(self):
        return "index, follow"

    def viewport(self):
        return "width=device-width, initial-scale=1, user-scalable=no"

    def og_title(self):
        return self.default_title[0]

    def og_description(self):
        return self.default_description

    def og_type(self):
        return self.default_og_type

    def og_image(self):
        return {
            "url": self.absolute_url(static('images/site/logo-200x200.png')),
            "secure_url": self.absolute_url(static('images/site/logo-200x200.png')),
            "type": 'image/png',
            "width": '200',
            "height": '200',
        }

    def og_url(self):
        return self.absolute_url(self.context['request'].path)

    def twitter_card(self):
        return "summary"

    def twitter_site(self):
        return self.default_site_twitter_handle

    def twitter_creator(self):
        return "@lvisintini"

    def twitter_title(self):
        return self.default_title[0]

    def twitter_description(self):
        return self.default_description

    def twitter_image(self):
        return self.absolute_url(static('images/site/logo-200x200.png'))

    def msapplication_TileColor(self):
        return settings.BRAND_COLOR

    def msapplication_TileImage(self):
        return self.absolute_url(static('favicons/mstile-144x144.png'))

    def msapplication_config(self):
        return self.absolute_url(reverse('pages:browserconfig.xml'))

    def theme_color(self):
        return settings.BRAND_COLOR

    def apple_touch_icon(self):
        return self.absolute_url(static('favicons/apple-touch-icon.png'))

    def icon(self):
        return [
            ('32x32', self.absolute_url(static('favicons/favicon-32x32.png'))),
            ('16x16', self.absolute_url(static('favicons/favicon-16x16.png'))),
        ]

    def manifest(self):
        return self.absolute_url(reverse('pages:manifest.json'))

    def mask_icon(self):
        return {
            "url": self.absolute_url(static('favicons/safari-pinned-tab.svg')),
            "color": settings.BRAND_COLOR
        }

    def shortcut_icon(self):
        return self.absolute_url(static('favicons/favicon.ico'))

    def canonical(self):
        return self.absolute_url(self.context['request'].path)


class RulesIndexMetaData(DefaultMetaData):
    def title(self):
        return self.separator.join(['Rules', ] + self.default_title)

    def keywords(self):
        return ','.join(['rule index', ] + self.default_keywords)

    def og_title(self):
        return self.separator.join(self.default_title + ['Rules index', ])

    def og_url(self):
        return self.absolute_url(self.context['request'].path)

    def twitter_title(self):
        return self.separator.join(self.default_title + ['Rules index', ])

    def twitter_description(self):
        return self.default_description


class RulesPageMetaData(DefaultMetaData):
    def __init__(self, context):
        super().__init__(context)
        self.rule_description = self.default_description

        if self.context['rule'].type != RULE_TYPES.CARD:
            self.rule_description = self.context['rule'].clauses.filter(
                group=CLAUSE_GROUPS.MAIN
            ).first().current_content.content
        else:
            self.rule_description = "{} ({}) card clarification/errata".format(
                self.context['rule'].name,
                dict(CARD_TYPES.as_choices)[self.context['rule'].card_type]
            )

    def title(self):
        return self.separator.join([self.context['rule'].name, ] + self.default_title)

    def description(self):
        return self.rule_description

    def keywords(self):
        return ','.join(
            [self.context['rule'].name, dict(RULE_TYPES.as_choices)[self.context['rule'].type]] + self.default_keywords
        )

    def og_title(self):
        return self.separator.join(self.default_title + [self.context['rule'].name, ])

    def og_description(self):
        return self.rule_description

    def twitter_title(self):
        return self.separator.join(self.default_title + [self.context['rule'].name, ])

    def twitter_description(self):
        return self.rule_description


METADATA_MAPPING = {
    "pages:index": RulesIndexMetaData,
    #"pages:styleguide": None,
    #"pages:resources": None,
    #"pages:contact": None,
    #"pages:wall-of-fame": None,
    #"pages:about": None,
    #"books:book": None,
    "rules:index": RulesIndexMetaData,
    "rules:rule": RulesPageMetaData,
    #"faqs:index": None,
}
