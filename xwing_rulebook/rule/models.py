from django.contrib.postgres.fields import JSONField
from django.db import models

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
    date = models.DateField()
    version = models.CharField(max_length=25)
    code = models.CharField(max_length=25, default='', unique=True)
    description = models.TextField(default='')

    def __str__(self):
        return self.code


class Rule(models.Model):
    name = models.CharField(max_length=125)
    related_topics = models.ManyToManyField('self', blank=True)
    expansion_rule = models.BooleanField(default=False)

    class Meta:
        ordering = ['name', ]

    @property
    def anchor_id(self):
        return '-'.join(self.name.lower().split())

    def to_markdown(self, add_anchors=True):
        context = {
            'rule': self,
            'add_anchors': add_anchors
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
    clause_content = models.ForeignKey(
        'rule.ClauseContent', related_name='current_clauses', null=True
    )

    class Meta:
        ordering = ['rule', 'order']
        unique_together = ('rule', 'order')

    @property
    def anchor_id(self):
        return '{}-{}'.format(self.rule.anchor_id, self.order)

    def __str__(self):
        return 'Rule "{}" Clause {}'.format(self.rule, self.order)


class ClauseContent(models.Model):
    clause = models.ForeignKey('rule.Clause', related_name='available_contents')
    title = models.CharField(max_length=125, null=True, blank=True)
    content = models.TextField(default='')
    source = models.ForeignKey('rule.Source')
    page = models.IntegerField(null=True, blank=True)
    keep_line_breaks = models.BooleanField(default=False)

    def __str__(self):
        if self.page is not None:
            return '{} (Page {})'.format(self.source.code, self.page)
        return self.source.code


# Deprecate
class Paragraph(models.Model):
    rule = models.ForeignKey('rule.Rule', related_name='paragraphs')
    order = models.IntegerField(default=0)
    format = JSONField(default={'type': 'text', 'level': 0})
    text = models.TextField(default='')
    sources = models.ManyToManyField(
        'rule.Source', related_name='paragraphs', through='rule.Reference'
    )
    needs_revision = models.BooleanField(default=False)

    class Meta:
        ordering = ['order', ]
        unique_together = ('rule', 'order')

    @property
    def anchor_id(self):
        return '{}-{}'.format(self.rule.anchor_id, self.order)

    @property
    def reference_text(self):
        return ', '.join([
            '{} (Page {})'.format(ref.source.code, ref.page)
            for ref in self.reference_set.all()
        ])

    def __str__(self):
        return 'Rule "{}" Paragraph {}'.format(self.rule, self.order)


# Deprecate
class Reference(models.Model):
    source = models.ForeignKey('rule.Source')
    paragraph = models.ForeignKey('rule.Paragraph')
    page = models.IntegerField(default=0)

    class Meta:
        ordering = ['source', 'page']

    def __str__(self):
        return 'Page {} - {}'.format(self.page, self.source)


class RuleBook(models.Model):
    name = models.CharField(max_length=125)
    code = models.CharField(max_length=25, default='', unique=True)
    version = models.CharField(max_length=25, null=True, blank=True)
    description = models.TextField(default='')
    rules = models.ManyToManyField(
        'rule.Rule', related_name='rule_books', through='rule.RuleBookRule'
    )

    def __str__(self):
        return self.name


class BookSection(models.Model):
    rule_book = models.ForeignKey('rule.RuleBook')
    order = models.IntegerField(default=0)
    title = models.CharField(max_length=125, null=True, blank=True)
    content = models.TextField(default='')
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


# Deprecate
class RuleBookRule(models.Model):
    rule_book = models.ForeignKey('rule.RuleBook')
    rule = models.ForeignKey('rule.Rule')
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order', ]

    def __str__(self):
        return '{}:{}'.format(self.rule_book, self.rule)
