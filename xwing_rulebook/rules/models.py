import re

from django.conf import settings
from django.db import models


class CLAUSE_TYPES:
    TEXT = 'text'
    UNORDERED_ITEM = 'item:ul'
    ORDERED_ITEM = 'item:ol'

    as_choices = (
        (TEXT, 'Text'),
        (UNORDERED_ITEM, 'Unordered Item'),
        (ORDERED_ITEM, 'Ordered Item'),
    )

    as_list = [
        TEXT,
        UNORDERED_ITEM,
        ORDERED_ITEM,
    ]

    MARKDOWN_PREFIX_TYPE_MAPPING = {
        TEXT: '',
        UNORDERED_ITEM: '- ',
        ORDERED_ITEM: '1. ',
    }


class SOURCE_TYPES:
    MANUAL = 'M'
    REFERENCE_CARD = 'RC'
    RULES_REFERENCE = 'RR'
    FAQ = 'FAQ'
    OTHER = 'OTHER'

    PRECEDENCE = [
        FAQ,
        RULES_REFERENCE,
        REFERENCE_CARD,
        MANUAL,
        OTHER,
    ]

    as_choices = (
        (MANUAL, 'Manual'),
        (REFERENCE_CARD, 'Reference Card'),
        (RULES_REFERENCE, 'Rules Reference'),
        (FAQ, 'FAQ'),
    )
    as_list = [
        MANUAL,
        REFERENCE_CARD,
        RULES_REFERENCE,
        FAQ,
        OTHER,
    ]


class RULE_TYPES:
    RULE = 'rule'
    RULE_CLARIFICATION = 'rule-clarification'
    CARD = 'card'

    as_choices = (
        (RULE, 'Rule'),
        (RULE_CLARIFICATION, 'Rule clarification'),
        (CARD, 'Card'),
    )

    as_list = [
        RULE,
        RULE_CLARIFICATION,
        CARD,
    ]


class CLAUSE_GROUPS:
    MAIN = 1
    IMAGES = 2
    CARD_ERRATA = 3
    CARD_CLARIFICATION = 4

    as_choices = (
        (MAIN, 'Main'),
        (IMAGES, 'Images'),
        (CARD_ERRATA, 'Card Errata'),
        (CARD_CLARIFICATION, 'Card Clarification'),
    )

    as_list = [
        MAIN,
        IMAGES,
        CARD_ERRATA,
        CARD_CLARIFICATION,
    ]


class Source(models.Model):
    name = models.CharField(max_length=125)
    date = models.DateField(blank=True, null=True)
    code = models.CharField(max_length=50, default='', unique=True)
    type = models.CharField(
        max_length=50, choices=SOURCE_TYPES.as_choices, default=SOURCE_TYPES.REFERENCE_CARD
    )
    processed = models.BooleanField(default=False)

    def __str__(self):
        return '{}-{}'.format(self.type, self.code)


class Rule(models.Model):
    name = models.CharField(max_length=125)
    slug = models.SlugField(max_length=125, default='', unique=True)
    preserve_name_case = models.BooleanField(default=False)
    expansion_rule = models.BooleanField(default=False)
    huge_ship_rule = models.BooleanField(default=False)
    type = models.CharField(max_length=25, choices=RULE_TYPES.as_choices, default=RULE_TYPES.RULE)

    related_rules = models.ManyToManyField('self', blank=True)

    related_pilots = models.ManyToManyField('integrations.Pilot', blank=True,
                                            related_name='related_rules')
    related_upgrades = models.ManyToManyField('integrations.Upgrade', blank=True,
                                              related_name='related_rules')
    related_damage_decks = models.ManyToManyField('integrations.DamageDeck', blank=True,
                                                  related_name='related_rules')
    related_conditions = models.ManyToManyField('integrations.Condition', blank=True,
                                                related_name='related_rules')

    class Meta:
        ordering = ['name', ]

    @property
    def anchor_id(self):
        return '-'.join(self.name.lower().split())

    @property
    def name_as_title(self):
        automata = re.compile(r' ?\(.*?\)')
        return automata.sub('', self.name)

    def __str__(self):
        return '[{}] {}'.format(dict(RULE_TYPES.as_choices).get(self.type, self.type), self.name)


class Clause(models.Model):
    rule = models.ForeignKey('rules.Rule', related_name='clauses')
    order = models.IntegerField(default=0)
    type = models.CharField(
        max_length=11, choices=CLAUSE_TYPES.as_choices, default=CLAUSE_TYPES.UNORDERED_ITEM
    )
    group = models.IntegerField(default=1, choices=CLAUSE_GROUPS.as_choices)
    expansion_related = models.BooleanField(default=False)
    indentation = models.IntegerField(default=0)
    ignore_title = models.BooleanField(default=False)
    needs_revision = models.BooleanField(default=False)
    available_contents = models.ManyToManyField('contents.Content', through='rules.ClauseContent')

    class Meta:
        ordering = ['rule', 'order']

    @property
    def anchor_id(self):
        return '{}-{}'.format(self.rule.anchor_id, self.order)

    @property
    def current_content(self):
        if not hasattr(self, '_current_content'):
            qs = ClauseContent.objects.filter(clause_id=self.id)
            qs = qs.annotate(
                release_date=models.Case(
                    models.When(
                        content__source__date=None,
                        then=models.Min('content__source__product__release_date', distinct=True)
                    ),
                    default='content__source__date'
                )
            )
            qs = qs.annotate(
                precedence=models.Case(
                    models.When(
                        content__source__type=SOURCE_TYPES.FAQ,
                        then=SOURCE_TYPES.PRECEDENCE.index(SOURCE_TYPES.FAQ)
                    ),
                    models.When(
                        content__source__type=SOURCE_TYPES.RULES_REFERENCE,
                        then=SOURCE_TYPES.PRECEDENCE.index(SOURCE_TYPES.RULES_REFERENCE)
                    ),
                    models.When(
                        content__source__type=SOURCE_TYPES.REFERENCE_CARD,
                        then=SOURCE_TYPES.PRECEDENCE.index(SOURCE_TYPES.REFERENCE_CARD)
                    ),
                    models.When(
                        content__source__type=SOURCE_TYPES.MANUAL,
                        then=SOURCE_TYPES.PRECEDENCE.index(SOURCE_TYPES.MANUAL)
                    ),
                    default=SOURCE_TYPES.PRECEDENCE.index(SOURCE_TYPES.OTHER),
                    output_field=models.IntegerField()
                )
            )

            qs = qs .order_by('-release_date', 'precedence')
            self._current_content = qs.first().content
        return self._current_content

    def __str__(self):
        return 'Rule "{}" Clause {}'.format(self.rule, self.order)


class ClauseContent(models.Model):
    clause = models.ForeignKey('rules.Clause')
    content = models.ForeignKey('contents.Content')
