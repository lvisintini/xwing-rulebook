from django.db import models
from django.conf import settings


class CLAUSE_TYPES:
    TEXT = 'text'
    UNORDERED_ITEM = 'item:ul'
    ORDERED_ITEM = 'item:ol'
    TABLE = 'table'

    as_choices = (
        (TEXT, 'Text'),
        (UNORDERED_ITEM, 'Unordered Item'),
        (ORDERED_ITEM, 'Ordered Item'),
        (TABLE, 'Table'),
    )

    as_list = [
        TEXT,
        UNORDERED_ITEM,
        ORDERED_ITEM,
        TABLE
    ]

    MARKDOWN_PREFIX_TYPE_MAPPING = {
        TEXT: '',
        TABLE: '',
        UNORDERED_ITEM: '- ',
        ORDERED_ITEM: '1. '
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
    CARD_CLARIFICATION = 'card-clarification'
    CARD_ERRATA = 'card-errata'

    as_choices = (
        (RULE, 'Rule'),
        (RULE_CLARIFICATION, 'Rule clarification'),
        (CARD_CLARIFICATION, 'Card clarification'),
        (CARD_ERRATA, 'Card errata'),
    )

    as_list = [
        RULE,
        RULE_CLARIFICATION,
        CARD_CLARIFICATION,
        CARD_ERRATA,
    ]


class Source(models.Model):
    name = models.CharField(max_length=125)
    date = models.DateField(blank=True, null=True)
    code = models.CharField(max_length=50, default='', unique=True)
    type = models.CharField(
        max_length=50, choices=SOURCE_TYPES.as_choices, default=SOURCE_TYPES.REFERENCE_CARD
    )
    processed = models.BooleanField(default=False)
    file = models.FilePathField(
        max_length=255,
        path=settings.INTERNAL_ASSETS_DIR,
        recursive=True,
        allow_folders=False,
        null=True,
        blank=True
    )

    def __str__(self):
        return '{}-{}'.format(self.type, self.code)


class Rule(models.Model):
    name = models.CharField(max_length=125)
    slug = models.SlugField(max_length=125, default='', unique=True)
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
    def card_images(self):
        if not hasattr(self, '_card_images'):
            template = 'xwing-data-images/{image}'

            card_relationships = [
                self.related_pilots,
                self.related_upgrades,
                self.related_damage_decks,
                self.related_conditions
            ]

            card_images = []
            for qs in card_relationships:
                card_images.extend([
                    (c.name, template.format(**c.json)) for c in qs.all() if c.json.get('image')
                ])

            self._card_images = dict(card_images)

        return self._card_images

    def __str__(self):
        return self.name


class Clause(models.Model):
    rule = models.ForeignKey('rules.Rule', related_name='clauses')
    order = models.IntegerField(default=0)
    type = models.CharField(
        max_length=10, choices=CLAUSE_TYPES.as_choices, default=CLAUSE_TYPES.UNORDERED_ITEM
    )
    expansion_related = models.BooleanField(default=False)
    indentation = models.IntegerField(default=0)
    ignore_title = models.BooleanField(default=False)
    needs_revision = models.BooleanField(default=False)
    available_contents = models.ManyToManyField('rules.Content', through='rules.ClauseContent')

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
    content = models.ForeignKey('rules.Content')


class Content(models.Model):
    title = models.CharField(max_length=125, null=True, blank=True)
    content = models.TextField(default='')
    source = models.ForeignKey('rules.Source')
    page = models.IntegerField(null=True, blank=True)
    keep_line_breaks = models.BooleanField(default=False)
    file = models.FilePathField(
        max_length=255,
        path=settings.STATICFILES_DIRS[0],
        recursive=True,
        allow_folders=False,
        null=True,
        blank=True
    )

    def __str__(self):
        reference = str(self.source)
        if self.page is not None:
            reference = '{} (Page {})'.format(reference, self.page)

        if self.title:
            return '{} - {}: {}'.format(reference, self.title, self.content)[:125]
        return '{} - {}'.format(reference, self.content[:125])
