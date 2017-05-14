from faqs.models import Faq, TOPICS
from itertools import groupby
from markdowns.base import MarkdownBase


class FaqsToMarkdown(MarkdownBase):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        qs = Faq.objects
        qs = qs.select_related('source')
        qs = qs.prefetch_related('related_clauses__rule')
        self.faqs = qs

    def topic_title(self, topic):
        template = '{header_level} {topic} {anchor}'
        return template.format(
            header_level='#' * (self.header_level + 1),
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
            self.faqs, key=lambda f: TOPICS.as_list.index(f.topic)
        )

        faqs_topic_mds = []
        for topic_index, group in faq_groups:
            topic_mds = [self.topic_title(TOPICS.as_list[topic_index]), ]
            for faq in group:
                topic_mds.append(self.faq_markdown(faq))
            faqs_topic_mds.append('\n'.join(topic_mds))

        return '\n\n'.join(faqs_topic_mds)

    def faq_markdown(self, faq):
        question = self.render_links(faq.question)
        answer = self.render_links(faq.answer)

        template = '**Q: {question}**{q_anchor}\nA:{answer}{a_anchor}\n{related}'

        return template.format(
            question=question,
            answer=answer,
            q_anchor='' if not self.anchored else '\n' + self.render_attrs(
                ids=['{}-Q-{}'.format(faq.anchor_id, faq.id), ],
                data={
                    'anchor-id': '{}-Q-{}'.format(faq.anchor_id, faq.id),
                    'source-code': faq.source.code,
                    'page': '' if faq.page is None else faq.page,
                    'id': faq.id,
                    'type': 'question',
                }
            ),
            a_anchor='' if not self.anchored else '\n' + self.render_attrs(
                ids=['{}-A-{}'.format(faq.anchor_id, faq.id), ],
                data={
                    'anchor-id': '{}-A-{}'.format(faq.anchor_id, faq.id),
                    'source-code': faq.source.code,
                    'page': '' if faq.page is None else faq.page,
                    'id': faq.id,
                    'type': 'answer',
                }
            ),
            related=self.faq_related_clauses(faq)
        )

    def faq_related_clauses(self, faq):
        return '**Related rules** {}'.format('<COMING-SOON>')
