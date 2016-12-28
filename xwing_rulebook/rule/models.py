from django.contrib.postgres.fields import JSONField
from django.db import models

from util.lib import render_template


class Source(models.Model):
    name = models.CharField(max_length=125)
    date = models.DateField()
    version = models.CharField(max_length=25)
    code = models.CharField(max_length=25, default='')
    description = models.TextField(default='')

    def __str__(self):
        return '{} ({})'.format(self.name, self.version)


class Rule(models.Model):
    name = models.CharField(max_length=125)
    related_topics = models.ManyToManyField('self', blank=True)
    expansion_rule = models.BooleanField(default=False)

    @property
    def anchor_id(self):
        return '-'.join(self.name.lower().split())

    def to_markdown(self):
        context = {
            'rule': self,
            'add_anchors': True
        }
        return render_template('markdown/rule.md', context).strip()

    def __str__(self):
        return self.name


class Paragraph(models.Model):
    rule = models.ForeignKey('rule.Rule', related_name='paragraphs')
    order = models.IntegerField(default=0)
    format = JSONField(default={'type': 'text', 'level': 0})
    text = models.TextField(default='')
    sources = models.ManyToManyField(
        'rule.Source', related_name='paragraphs', through='rule.Reference'
    )

    class Meta:
        ordering = ['order', ]
        unique_together = ("rule", "order")

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


class Reference(models.Model):
    source = models.ForeignKey('rule.Source')
    paragraph = models.ForeignKey('rule.Paragraph')
    page = models.IntegerField(default=0)

    def __str__(self):
        return 'Page {} - {}'.format(self.page, self.source)


class RuleBook(models.Model):
    name = models.CharField(max_length=125)
    version = models.CharField(max_length=25, null=True, blank=True)
    description = models.TextField(default='')
    rules = models.ManyToManyField(
        'rule.Rule', related_name='rule_books', through='rule.RuleBookRule'
    )

    def __str__(self):
        return self.name


class RuleBookRule(models.Model):
    rule_book = models.ForeignKey('rule.RuleBook')
    rule = models.ForeignKey('rule.Rule')
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order', ]
