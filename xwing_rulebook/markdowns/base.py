from django.urls import reverse
from django.utils.functional import cached_property

from contents.models import Link


class MarkdownBase:
    default_url_name = None

    def __init__(self, **kwargs):
        self.header_level = kwargs.pop('header_level', 3)
        self.anchored = kwargs.pop('anchored', False)
        self.linked = kwargs.pop('linked', False)
        self.anchored_links = kwargs.pop('anchored_links', False)
        self.url_name = kwargs.pop('url_name', self.default_url_name)
        self.extra_url_params = kwargs

    @staticmethod
    def render_attrs(ids=None, classes=None, data=None):
        ids = ids or []
        classes = classes or []
        data = data or {}

        template = "{{: {ids} {classes} {data} }}"

        return template.format(
            ids=' '.join(['#{}'.format(x) for x in ids]) if ids else '',
            classes=' '.join(['.{}'.format(x) for x in classes]) if classes else '',
            data=' '.join(
                ['data-{}="{}"'.format(k, v) for k, v in data.items() if v or v == 0]
            ) if data else '',
        )

    def render_link(self, link):
        templates = {
            (False, False, False): '{text}',
            (False, False, True): '[{text}]({url})',
            (False, True, False): '{text}',
            (False, True, True): '[{text}]({url})',

            (True, False, False): '{rule}{expansion_icon}',
            (True, False, True): '[{rule}{expansion_icon}]({relative_url})',
            (True, True, False): '[{rule}{expansion_icon}](#{anchor})',
            (True, True, True): '[{rule}{expansion_icon}]({relative_url}#{anchor})',
        }

        template = templates[(bool(link.rule), self.anchored_links, self.linked)]
        url_params = list(self.extra_url_params.items())

        return template.format(
            rule=link.rule.name if link.rule else link.text,
            expansion_icon='†' if link.rule and link.rule.expansion_rule else '',
            relative_url=reverse(
                self.url_name, kwargs=dict([('rule_slug', link.rule.slug)] + url_params)
            ) if link.rule else '',
            anchor=link.rule.anchor_id if link.rule else '',
            url=link.url,
            text=link.text
        )

    @cached_property
    def links(self):
        return Link.objects.select_related('rule').all()

    def render_links(self, text):
        for l in self.links:
            text = text.replace(
                '<LINK:{}>'.format(l.alias), self.render_link(l)
            )
        return text