from django.db import models

from faqs.constants import TOPICS


class FaqManager(models.Manager):
    def get_queryset(self):
        qs = super().get_queryset()
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
        return qs


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

    objects = FaqManager()

    def __str__(self):
        return '[{}] Q:{}'.format(self.topic, self.question[:20])

    @property
    def anchor_id(self):
        return 'faq-{}-{}'.format(self.topic, self.id)
