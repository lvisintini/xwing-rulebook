from itertools import groupby
from collections import defaultdict

from django.db import models
from django.urls import reverse

from faqs.models import Faq
from faqs.constants import TOPICS
from markdowns.base import MarkdownBase


class FaqsToMarkdown(MarkdownBase):
    default_url_name = 'rules:rule'

    def __init__(self, **kwargs):
        qs = kwargs.pop('faqs', Faq.objects)
        qs = qs.annotate(
            topic_order=models.Case(
                models.When(
                    topic=TOPICS.GENERAL,
                    then=TOPICS.as_list.index(TOPICS.GENERAL)
                ),
                models.When(
                    topic=TOPICS.ACTIONS_AND_GAME_EFFECTS,
                    then=TOPICS.as_list.index(TOPICS.ACTIONS_AND_GAME_EFFECTS)
                ),
                models.When(
                    topic=TOPICS.COMBAT,
                    then=TOPICS.as_list.index(TOPICS.COMBAT)
                ),
                models.When(
                    topic=TOPICS.ATTACK_TIMING_CHART,
                    then=TOPICS.as_list.index(TOPICS.ATTACK_TIMING_CHART)
                ),
                models.When(
                    topic=TOPICS.MISSIONS,
                    then=TOPICS.as_list.index(TOPICS.MISSIONS)
                ),
                models.When(
                    topic=TOPICS.MOVEMENT,
                    then=TOPICS.as_list.index(TOPICS.MOVEMENT)
                ),
                models.When(
                    topic=TOPICS.RANGE_MEASUREMENT,
                    then=TOPICS.as_list.index(TOPICS.RANGE_MEASUREMENT)
                ),
                default=100,
                output_field=models.IntegerField()
            )
        )

        qs = qs.select_related('source')
        qs = qs.prefetch_related('related_clauses__rule')
        qs = qs.order_by('topic_order', 'order')

        self.faqs = qs
        super().__init__(**kwargs)

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
            self.faqs, key=lambda f: f.topic
        )

        faqs_topic_mds = []
        for topic, group in faq_groups:
            topic_mds = [self.faq_markdown(faq) for faq in group]
            faqs_topic_mds.append(
                '{}\n\n{}'.format(self.topic_title(topic), '\n\n----------\n\n'.join(topic_mds))
            )

        return '\n\n'.join(faqs_topic_mds)

    def faq_markdown(self, faq):
        question = self.render_links(faq.question)
        answer = self.render_links(faq.answer)

        template = '**Q: {question}**{q_anchor}\n\nA: {answer}{a_anchor}\n\n{related}'

        return template.format(
            question=question,
            answer=answer,
            q_anchor='' if not self.anchored else '\n' + self.render_attrs(
                ids=['{}-Q-{}'.format(faq.anchor_id, faq.id), ],
                data={
                    'anchor-id': '{}-Q'.format(faq.anchor_id),
                    'source-code': faq.source.code,
                    'page': '' if faq.page is None else faq.page,
                    'id': faq.id,
                    'type': 'question',
                }
            ),
            a_anchor='' if not self.anchored else '\n' + self.render_attrs(
                ids=['{}-A-{}'.format(faq.anchor_id, faq.id), ],
                data={
                    'anchor-id': '{}-A'.format(faq.anchor_id),
                    'source-code': faq.source.code,
                    'page': '' if faq.page is None else faq.page,
                    'id': faq.id,
                    'type': 'answer',
                }
            ),
            related=self.related_clauses_as_references(faq)
        )

    def related_clauses_as_references(self, faq):
        related = defaultdict(list)
        for rule in faq.related_rules.all():
            related[rule] = []

        for clause in faq.related_clauses.all():
            related[clause.rule].append(clause)

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
