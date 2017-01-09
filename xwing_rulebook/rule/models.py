from django.db import models
from django.conf import settings

from util.lib import render_template


CLAUSE_TYPES = (
    ('text', 'Text'),
    ('item:ul', 'Unordered Item'),
    ('item:ol', 'Ordered Item'),
    ('image', 'Image'),
    ('table', 'Table'),
)


class Source(models.Model):
    name = models.CharField(max_length=125)
    date = models.DateField(blank=True, null=True)
    version = models.CharField(max_length=25, blank=True, null=True)
    code = models.CharField(max_length=50, default='', unique=True)
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
        return self.code


class Rule(models.Model):
    name = models.CharField(max_length=125)
    slug = models.SlugField(max_length=125, default='', unique=True)
    related_topics = models.ManyToManyField('self', blank=True)
    expansion_rule = models.BooleanField(default=False)

    class Meta:
        ordering = ['name', ]

    @property
    def anchor_id(self):
        return '-'.join(self.name.lower().split())

    def to_markdown(self, add_anchors=True, rulebook=None, section=None):
        context = {
            'rule': self,
            'add_anchors': add_anchors,
            'rulebook': rulebook,
            'section': section,
        }
        return render_template('markdown/rule.md', context).strip()

    def __str__(self):
        return self.name


class Clause(models.Model):
    rule = models.ForeignKey('rule.Rule', related_name='clauses')
    order = models.IntegerField(default=0)
    type = models.CharField(max_length=10, choices=CLAUSE_TYPES, default='item:ul')
    expansion_related = models.BooleanField(default=False)
    indentation = models.IntegerField(default=0)
    ignore_title = models.BooleanField(default=False)
    needs_revision = models.BooleanField(default=False)
    available_contents = models.ManyToManyField('rule.ClauseContent',
                                                through='rule.ClauseContentVersion')

    class Meta:
        ordering = ['rule', 'order']

    @property
    def anchor_id(self):
        return '{}-{}'.format(self.rule.anchor_id, self.order)

    def __str__(self):
        return 'Rule "{}" Clause {}'.format(self.rule, self.order)


class ClauseContentVersion(models.Model):
    clause = models.ForeignKey('rule.Clause')
    content = models.ForeignKey('rule.ClauseContent')
    active = models.BooleanField(default=False)

    class Meta:
        ordering = ['active']


class ClauseContent(models.Model):
    title = models.CharField(max_length=125, null=True, blank=True)
    content = models.TextField(default='')
    source = models.ForeignKey('rule.Source')
    page = models.IntegerField(null=True, blank=True)
    keep_line_breaks = models.BooleanField(default=False)
    file = models.FilePathField(
        path=settings.INTERNAL_ASSETS_DIR,
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


class RuleBook(models.Model):
    name = models.CharField(max_length=125, unique=True)
    slug = models.SlugField(max_length=125, unique=True, default='')
    code = models.CharField(max_length=25, default='', unique=True)
    version = models.CharField(max_length=25, null=True, blank=True)
    description = models.TextField(default='')

    def has_rule(self, rule):
        pass

    def __str__(self):
        return self.name

    @property
    def rule_ids(self):
        if not hasattr(self, '_rules'):
            section_ids = self.booksection_set.values_list('id', flat=True)
            self._rule_ids = SectionRule.objects.filter(
                book_section_id__in=section_ids
            ).values_list('rule_id', flat=True)

        return self._rule_ids


class BookSection(models.Model):
    rule_book = models.ForeignKey('rule.RuleBook')
    order = models.IntegerField(default=0)
    title = models.CharField(max_length=125, null=True, blank=True)
    slug = models.SlugField(max_length=125, unique=True, default='')
    content = models.TextField(default='', blank=True)
    rules = models.ManyToManyField('rule.Rule', through='rule.SectionRule')

    class Meta:
        ordering = ['order', ]

    def __str__(self):
        return '{}: {}'.format(self.rule_book, self.title)


class SectionRule(models.Model):
    book_section = models.ForeignKey('rule.BookSection')
    rule = models.ForeignKey('rule.Rule')
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order', ]

    def __str__(self):
        return '{}: {}'.format(self.book_section, self.rule)
