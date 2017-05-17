from django.db import models

from faqs.constants import TOPICS


class Faq(models.Model):
    topic = models.CharField(max_length=24, choices=TOPICS.as_choices, default=TOPICS.GENERAL)
    question = models.TextField(default='')
    answer = models.TextField(default='')
    question_as_per_source = models.TextField(
        default='',
        help_text="If the text in the question field is not a verbatim copy of the source's text, "
                  "Add the original text here.",
        blank=True
    )
    answer_as_per_source = models.TextField(
        default='',
        help_text="If the text in the answer field is not a verbatim copy of the source's text, "
                  "Add the original text here.",
        blank=True
    )
    source = models.ForeignKey('rules.Source', related_name="faqs")
    page = models.IntegerField(null=True, blank=True)
    order = models.IntegerField(default=0)
    related_clauses = models.ManyToManyField('rules.Clause', blank=True, related_name='faqs')
    related_rules = models.ManyToManyField('rules.Rule', blank=True, related_name='faqs')

    def __str__(self):
        return '[{}] Q:{}'.format(self.topic, self.question[:20])

    @property
    def anchor_id(self):
        return 'faq-{}-{}'.format(self.topic, self.id)
