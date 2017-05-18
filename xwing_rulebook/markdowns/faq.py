from itertools import groupby
from collections import defaultdict, OrderedDict

from django.db import models
from django.urls import reverse

from faqs.models import Faq
from faqs.constants import TOPICS
from markdowns.base import MarkdownBase


class Faq2Markdown(MarkdownBase):
    default_url_name = 'rules:rule'

    def __init__(self, faq, **kwargs):
        self.faq = faq
        super().__init__(**kwargs)

    def faq_markdown(self):
        question = self.render_links(self.faq.question)
        answer = self.render_links(self.faq.answer)

        template = '**Q: {question}**{q_anchor}\n\nA: {answer}{a_anchor}'

        return template.format(
            question=question,
            answer=answer,
            q_anchor='' if not self.anchored else '\n' + self.render_attrs(
                ids=['{}-Q-{}'.format(self.faq.anchor_id, self.faq.id), ],
                data={
                    'anchor-id': '{}-Q'.format(self.faq.anchor_id),
                    'source-code': self.faq.source.code,
                    'page': '' if self.faq.page is None else self.faq.page,
                    'id': self.faq.id,
                    'type': 'question',
                }
            ),
            a_anchor='' if not self.anchored else '\n' + self.render_attrs(
                ids=['{}-A-{}'.format(self.faq.anchor_id, self.faq.id), ],
                data={
                    'anchor-id': '{}-A'.format(self.faq.anchor_id),
                    'source-code': self.faq.source.code,
                    'page': '' if self.faq.page is None else self.faq.page,
                    'id': self.faq.id,
                    'type': 'answer',
                }
            ),
        )

    def related_rules_as_references(self):
        related = defaultdict(list)
        for rule in self.faq.related_rules.all():
            related[rule] = []

        for clause in self.faq.related_clauses.all():
            related[clause.rule].append(clause)

        related = OrderedDict(sorted(related.items(), key=lambda x: x[0].name))

        templates = {
            (False, False): '{rule}{expansion_icon}',
            (True, False): '[{rule}{expansion_icon}]({anchor})',
            (False, True): '[{rule}{expansion_icon}]({relative_url})',
            (True, True): '[{rule}{expansion_icon}]({relative_url}{anchor})',
        }

        template = templates[(self.anchored_links, self.linked)]
        url_params = list(self.extra_url_params.items())

        references = ', '.join([
            template.format(
                rule=rule.name,
                expansion_icon='' if not rule.expansion_rule else '†',
                relative_url=reverse(
                    self.url_name, kwargs=dict([('rule_slug', rule.slug)] + url_params)
                ),
                anchor='#{}'.format('&'.join([c.anchor_id for c in clauses])) if clauses else '',
            )
            for rule, clauses in related.items()
        ])

        return '**Related Rules:** {}'.format(references)


class Faqs2Markdown(MarkdownBase):
    default_url_name = 'rules:rule'

    def __init__(self, faqs=None, **kwargs):
        super().__init__(**kwargs)

        qs = Faq.objects if faqs is None else faqs
        qs = qs.select_related('source')
        qs = qs.prefetch_related('related_clauses__rule')
        qs = qs.order_by('topic_order', 'order')

        self.faq_helpers = []

        for faq in qs.all():
            self.faq_helpers.append(
                Faq2Markdown(
                    faq,
                    header_level=self.header_level + 1,
                    anchored=self.anchored,
                    linked=self.linked,
                    anchored_links=self.anchored_links,
                    url_name=self.url_name,
                    **self.extra_url_params
                )
            )

    def topic_title(self, topic):
        template = '{header_level} {topic} {anchor}'
        return template.format(
            header_level='#' * self.header_level,
            topic=dict(TOPICS.as_choices)[topic],
            anchor='' if not self.anchored else self.render_attrs(
                ids=['faq-{}'.format(topic), ],
                classes=[],
                data={
                    'order': TOPICS.as_list.index(topic)
                }
            ),
        )

    def faqs_markdown(self):
        faq_groups = groupby(
            self.faq_helpers, key=lambda fh: fh.faq.topic
        )

        faqs_topic_mds = []
        for topic, group in faq_groups:
            topic_mds = [
                faq_helper.faq_markdown() + '\n\n' + faq_helper.related_rules_as_references()
                for faq_helper in group
            ]
            faqs_topic_mds.append(
                '{}\n\n{}'.format(self.topic_title(topic), '\n\n----------\n\n'.join(topic_mds))
            )

        return '\n\n'.join(faqs_topic_mds)
