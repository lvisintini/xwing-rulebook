from django.db import models
from django.conf import settings
from django.urls import reverse
from django.contrib.staticfiles.templatetags.staticfiles import static


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
    EXAMPLE = 'example'

    as_choices = (
        (RULE, 'Rule'),
        (RULE_CLARIFICATION, 'Rule clarification'),
        (CARD_CLARIFICATION, 'Card clarification'),
        (EXAMPLE, 'Example'),
    )

    as_list = [
        RULE,
        RULE_CLARIFICATION,
        CARD_CLARIFICATION,
        EXAMPLE,
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

    class Meta:
        ordering = ['name', ]

    @property
    def anchor_id(self):
        return '-'.join(self.name.lower().split())

    def as_anchored_markdown(self):
        return self.to_markdown(True)

    def as_unanchored_markdown(self):
        return self.to_markdown(False)

    def to_markdown(self, add_anchors):
        template = '### {anchor}{rule_name}{expansion_rule}\n{clauses}'
        anchor_template = '<a id="{anchor_id}"></a>'

        return template.format(
            anchor='' if not add_anchors else anchor_template.format(anchor_id=self.anchor_id),
            rule_name=self.name,
            expansion_rule='' if not self.expansion_rule else ' †',
            clauses='\n'.join([c.to_markdown(add_anchors) for c in self.clauses.all()])
        )

    def related_topics_ss(self, add_anchors, add_links, url_name='rules:rule', **extra_url_params):
        related_topics = self.related_topics.filter(type=RULE_TYPES.RULE)

        if not related_topics.count():
            return ''

        topics = '**Related Topics:** {}'
        templates = {
            (False, False): '{rule}{expansion_icon}',
            (True, False): '[{rule}{expansion_icon}](#{anchor})',
            (False, True): '[{rule}{expansion_icon}]({relative_url})',
            (True, True): '[{rule}{expansion_icon}]({relative_url}#{anchor})',
        }

        template = templates[(add_anchors, add_links)]

        url_params = list(extra_url_params.items())

        topics = topics.format(', '.join([
            template.format(
                rule=r,
                expansion_icon='' if not r.expansion_rule else '†',
                relative_url=reverse(url_name, kwargs=dict([('rule_slug', r.slug)] + url_params)),
                anchor=r.anchor_id,
            )
            for r in related_topics
        ]))

        return topics

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

    def to_markdown(self, add_anchors):
        content = self.current_content

        template = '{indentation}{prefix}{anchor}{title}{content}'
        anchor_template = '<a class="SourceReference" id="{anchor_id}">' \
                          '{source_code}{page}{clause}</a>'

        file = ''
        if content.file:
            file = static(content.file.replace(settings.STATICFILES_DIRS[0], ''))

        res = template.format(
            indentation='    ' * self.indentation,
            prefix=CLAUSE_TYPES.MARKDOWN_PREFIX_TYPE_MAPPING[self.type],
            anchor='' if not add_anchors else anchor_template.format(
                anchor_id=self.anchor_id,
                source_code=content.source.code,
                page='' if content.page is None else ' (Page {})'.format(content.page),
                clause=' [{}]'.format(self.id)
            ),
            title='' if not content.title or self.ignore_title else '**{}{}:** '.format(
                content.title, '†' if self.expansion_related else ''
            ),
            content=content.content.replace('<FILE>', file),
        )
        return res

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
