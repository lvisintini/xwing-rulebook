from django.db import models


class TOPICS:
    GENERAL = "general"
    ACTIONS_AND_GAME_EFFECTS = "actions-and-game-effects"
    COMBAT = "Combat"
    ATTACK_TIMING_CHART = "attack-timing-chart"
    MISSIONS = "missions"
    MOVEMENT = "movement"
    RANGE_MEASUREMENT = "range-measurement"

    as_choices = (
        (GENERAL, 'General'),
        (ACTIONS_AND_GAME_EFFECTS, 'Actions and game effects'),
        (COMBAT, 'Combat'),
        (ATTACK_TIMING_CHART, 'Timing chart for performing an attack'),
        (MISSIONS, 'Missions'),
        (MOVEMENT, 'Movement'),
        (RANGE_MEASUREMENT, 'Range measurement'),
    )

    as_list = [
        GENERAL,
        ACTIONS_AND_GAME_EFFECTS,
        COMBAT,
        ATTACK_TIMING_CHART,
        MISSIONS,
        MOVEMENT,
        RANGE_MEASUREMENT
    ]


class Faq(models.Model):
    topic = models.CharField(max_length=24, choices=TOPICS.as_choices, default=TOPICS.GENERAL)
    question = models.TextField(default='')
    answer = models.TextField(default='')
    source = models.ForeignKey('rules.Source', related_name="faqs")
    page = models.IntegerField(null=True, blank=True)
    order = models.IntegerField(default=0)
    related_clauses = models.ManyToManyField('rules.Clause', blank=True)

    def __str__(self):
        return '[{}] Q:{}'.format(self.topic, self.question[:20])
