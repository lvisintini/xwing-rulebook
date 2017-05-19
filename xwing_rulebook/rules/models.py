import re

from django.db import models
from django.utils.functional import cached_property

from rules.constants import CLAUSE_TYPES, SOURCE_TYPES, RULE_TYPES, CLAUSE_GROUPS, CARD_TYPES


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


class RuleManager(models.Manager):
    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.annotate(
            type_order=models.Case(
                models.When(
                    type=RULE_TYPES.RULE,
                    then=RULE_TYPES.as_list.index(RULE_TYPES.RULE)
                ),
                models.When(
                    type=RULE_TYPES.RULE_CLARIFICATION,
                    then=RULE_TYPES.as_list.index(RULE_TYPES.RULE)
                ),
                models.When(
                    type=RULE_TYPES.CARD,
                    then=RULE_TYPES.as_list.index(RULE_TYPES.CARD)
                ),
                default=100,
                output_field=models.IntegerField()
            )
        )

        qs = qs.annotate(
            card_type_order=models.Case(
                models.When(
                    card_type=CARD_TYPES.NOT_APPLICABLE,
                    then=CARD_TYPES.as_list.index(CARD_TYPES.NOT_APPLICABLE)
                ),
                models.When(
                    card_type=CARD_TYPES.DAMAGE_ORG,
                    then=CARD_TYPES.as_list.index(CARD_TYPES.DAMAGE_ORG)
                ),
                models.When(
                    card_type=CARD_TYPES.DAMAGE_TFA,
                    then=CARD_TYPES.as_list.index(CARD_TYPES.DAMAGE_TFA)
                ),
                models.When(
                    card_type=CARD_TYPES.CONDITION,
                    then=CARD_TYPES.as_list.index(CARD_TYPES.CONDITION)
                ),
                models.When(
                    card_type=CARD_TYPES.PILOT,
                    then=CARD_TYPES.as_list.index(CARD_TYPES.PILOT)
                ),
                models.When(
                    card_type=CARD_TYPES.UPGRADE,
                    then=CARD_TYPES.as_list.index(CARD_TYPES.UPGRADE)
                ),
                default=100,
                output_field=models.IntegerField()
            )
        )
        return qs


class Rule(models.Model):
    name = models.CharField(max_length=125)
    slug = models.SlugField(max_length=125, default='', unique=True)
    preserve_name_case = models.BooleanField(default=False)
    expansion_rule = models.BooleanField(default=False)
    huge_ship_rule = models.BooleanField(default=False)
    type = models.CharField(max_length=25, choices=RULE_TYPES.as_choices, default=RULE_TYPES.RULE)
    card_type = models.IntegerField(
        default=CARD_TYPES.NOT_APPLICABLE, choices=CARD_TYPES.as_choices, blank=False, null=False
    )
    related_rules = models.ManyToManyField('self', blank=True)
    additional_keywords = models.CharField(max_length=250, default='', blank=True)

    objects = RuleManager()

    class Meta:
        ordering = ['name', ]

    @property
    def anchor_id(self):
        return '-'.join(self.name.lower().split())

    @property
    def name_as_title(self):
        automata = re.compile(r' ?\(.*?\)')
        return automata.sub('', self.name)

    @cached_property
    def related_faqs(self):
        faqs = self.faqs.all().distinct()
        for c in self.clauses.prefetch_related('faqs').all():
            faqs = faqs | c.faqs.all().distinct()

        if self.type == RULE_TYPES.RULE:
            for clarification in self.related_rules.filter(type=RULE_TYPES.RULE_CLARIFICATION):
                faqs = faqs | clarification.related_faqs

        return faqs

    @cached_property
    def extended_clauses(self):
        clauses = self.clauses.all()

        if self.type == RULE_TYPES.RULE:
            for clarification in self.related_rules.filter(type=RULE_TYPES.RULE_CLARIFICATION):
                clauses = clauses | clarification.clauses.all()

        return clauses

    def __str__(self):
        return '[{}] {}'.format(dict(RULE_TYPES.as_choices).get(self.type, self.type), self.name)


class Clause(models.Model):
    rule = models.ForeignKey('rules.Rule', related_name='clauses')
    order = models.IntegerField(default=0)
    type = models.CharField(
        max_length=11, choices=CLAUSE_TYPES.as_choices, default=CLAUSE_TYPES.TEXT
    )
    group = models.IntegerField(choices=CLAUSE_GROUPS.as_choices, default=CLAUSE_GROUPS.MAIN)
    expansion_related = models.BooleanField(default=False)
    indentation = models.IntegerField(default=0)
    ignore_title = models.BooleanField(default=False)
    needs_revision = models.BooleanField(default=False)
    available_contents = models.ManyToManyField('contents.Content', through='rules.ClauseContent')

    class Meta:
        ordering = ['rule', 'order']

    @cached_property
    def anchor_id(self):
        return '{}-{}'.format(self.rule.anchor_id, self.id)

    @cached_property
    def current_content(self):
        qs = self.available_contents.select_related('source')

        qs = qs.annotate(
            release_date=models.Case(
                models.When(
                    source__date=None,
                    then=models.Min('source__products__release_date', distinct=True)
                ),
                default='source__date'
            )
        )
        qs = qs.annotate(
            precedence=models.Case(
                models.When(
                    source__type=SOURCE_TYPES.FAQ,
                    then=SOURCE_TYPES.PRECEDENCE.index(SOURCE_TYPES.FAQ)
                ),
                models.When(
                    source__type=SOURCE_TYPES.RULES_REFERENCE,
                    then=SOURCE_TYPES.PRECEDENCE.index(SOURCE_TYPES.RULES_REFERENCE)
                ),
                models.When(
                    source__type=SOURCE_TYPES.REFERENCE_CARD,
                    then=SOURCE_TYPES.PRECEDENCE.index(SOURCE_TYPES.REFERENCE_CARD)
                ),
                models.When(
                    source__type=SOURCE_TYPES.MANUAL,
                    then=SOURCE_TYPES.PRECEDENCE.index(SOURCE_TYPES.MANUAL)
                ),
                default=SOURCE_TYPES.PRECEDENCE.index(SOURCE_TYPES.OTHER),
                output_field=models.IntegerField()
            )
        )

        qs = qs .order_by('-release_date', 'precedence')

        return qs.first()

    def __str__(self):
        return 'Rule "{}" Clause {}'.format(self.rule, self.order)


class ClauseContent(models.Model):
    clause = models.ForeignKey('rules.Clause', related_name='clause_contents')
    content = models.ForeignKey('contents.Content')
