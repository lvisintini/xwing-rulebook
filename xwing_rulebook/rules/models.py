import re

from django.contrib.staticfiles.templatetags.staticfiles import static
from django.db import models
from django.utils.functional import cached_property

from rules.constants import CLAUSE_TYPES, SOURCE_TYPES, RULE_TYPES, CLAUSE_GROUPS, CARD_TYPES, SOURCE_STATUS


class EnrichedSourceManager(models.Manager):
    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.prefetch_related('products')

        qs = qs.annotate(content_count=models.Count('contents'))

        qs = qs.annotate(
            release_date=models.Case(
                models.When(date=None, then=models.Min('products__release_date', distinct=True)),
                default='date'
            )
        )
        qs = qs.annotate(
            precedence=models.Case(
                *[
                    models.When(
                        type=st,
                        then=SOURCE_TYPES.PRECEDENCE.index(st)
                    )
                    for st in SOURCE_TYPES.PRECEDENCE
                    if st != SOURCE_TYPES.OTHER
                ],
                default=SOURCE_TYPES.PRECEDENCE.index(SOURCE_TYPES.OTHER),
                output_field=models.IntegerField()
            )
        )

        qs = qs.order_by('-release_date', 'precedence')
        return qs


class Source(models.Model):
    name = models.CharField(max_length=125)
    date = models.DateField(blank=True, null=True)
    code = models.CharField(max_length=50, default='', unique=True)
    status = models.IntegerField(choices=SOURCE_STATUS.as_admin_choices, default=SOURCE_STATUS.MISSING)
    type = models.CharField(
        max_length=50, choices=SOURCE_TYPES.as_choices, default=SOURCE_TYPES.REFERENCE_CARD
    )
    file = models.CharField(max_length=255, null=True, blank=True)
    notes = models.CharField(max_length=250, default='', blank=True)

    objects = models.Manager()
    enriched = EnrichedSourceManager()

    @property
    def status_readable(self):
        return dict(SOURCE_STATUS.as_user_choices)[self.status]

    @property
    def status_icon(self):
        return dict(SOURCE_STATUS.as_user_icons).get(self.status, 'fa-question')

    def __str__(self):
        return '{}-{}'.format(self.type, self.code)

    @cached_property
    def static_file(self):
        if self.file:
            return static(self.file)
        return None


class RuleManager(models.Manager):
    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.annotate(
            type_order=models.Case(
                *[
                    models.When(
                        type=rt,
                        then=RULE_TYPES.as_list.index(rt)
                    )
                    for rt in RULE_TYPES.as_list
                ],
                default=100,
                output_field=models.IntegerField()
            )
        )

        qs = qs.annotate(
            card_type_order=models.Case(
                *[
                    models.When(
                        type=ct,
                        then=CARD_TYPES.as_list.index(ct)
                    )
                    for ct in CARD_TYPES.as_list
                ],
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

    @property
    def decorated_name(self):
        template = '{rule_name}{expansion_rule}{huge_ship}'
        return template.format(
            rule_name=self.name,
            expansion_rule='' if not self.expansion_rule else ' ^†^',
            huge_ship='' if not self.huge_ship_rule else ' ^[Epic]^',
        )

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
                *[
                    models.When(
                        source__type=st,
                        then=SOURCE_TYPES.PRECEDENCE.index(st)
                    )
                    for st in SOURCE_TYPES.PRECEDENCE
                    if st != SOURCE_TYPES.OTHER
                ],
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
