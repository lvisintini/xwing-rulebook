from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from rules.models import Rule, Source
from rules.constants import SOURCE_TYPES


class RulesSitemap(Sitemap):
    changefreq = "monthy"
    priority = 1

    def items(self):
        return Rule.objects.order_by('type_order', 'card_type_order', 'name')

    def lastmod(self, obj):
        return obj.last_updated

    def location(self, obj):
        return reverse('rules:rule', args=[], kwargs={'rule_slug': obj.slug})


class FAQsSitemap(Sitemap):
    priority = 0.9
    changefreq = 'monthy'

    def items(self):
        return ['faqs:index', ]

    def lastmod(self, obj):
        return Source.enriched.filter(type=SOURCE_TYPES.FAQ).first().release_date

    def location(self, item):
        return reverse(item)


class PagesSitemap(Sitemap):
    priority = 0.5
    changefreq = 'monthy'

    def items(self):
        return [
            'pages:resources',
            'pages:maneuvers',
            'pages:wall-of-fame',
            'rules:index',
        ]

    def location(self, item):
        return reverse(item)


class CorollarySitemap(Sitemap):
    priority = 0.1
    changefreq = 'yearly'

    def items(self):
        return [
            'pages:index',
            'pages:contact',
            'pages:about',
        ]

    def location(self, item):
        return reverse(item)

sitemaps = {
    'rules': RulesSitemap,
    'faqs': FAQsSitemap,
    'pages': PagesSitemap,
    'static': CorollarySitemap,
}
