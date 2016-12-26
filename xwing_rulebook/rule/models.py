from django.contrib.postgres.fields import JSONField
from django.db import models

from util.lib import render_template


class Source(models.Model):
    name = models.CharField(max_length=125)
    date = models.DateField()
    version = models.CharField(max_length=25)
    description = models.TextField(default='')

    def __str__(self):
        return '{} ({})'.format(self.name, self.version)


class Rule(models.Model):
    name = models.CharField(max_length=125)
    related_topics = models.ForeignKey('rule.Rule', null=True, blank=True)
    expansion_rule = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def to_markdown(self):
        context = {
            'rule': self,
        }
        return render_template('markdown/rule.md', context).strip()


class Paragraph(models.Model):
    rule = models.ForeignKey('rule.Rule', related_name='paragraphs')
    order = models.IntegerField(default=0)
    format = JSONField(default={'type': 'text', 'level': 0})
    text = models.TextField(default='')
    sources = models.ManyToManyField(
        'rule.Source', related_name='paragraphs', through='rule.Reference'
    )

    def __str__(self):
        return 'Rule "{}" Paragraph {}'.format(self.rule, self.order)

    def to_markdown(self):
        pass


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
