from django.db import models
from django.utils.functional import cached_property


class Book(models.Model):
    name = models.CharField(max_length=125, unique=True)
    slug = models.SlugField(max_length=125, unique=True, default='')
    code = models.CharField(max_length=25, default='', unique=True)
    version = models.CharField(max_length=25, null=True, blank=True)
    description = models.TextField(default='')

    def __str__(self):
        return self.name

    @cached_property
    def rule_ids(self):
        section_ids = self.section_set.values_list('id', flat=True)
        return list(set(SectionRule.objects.filter(
            section_id__in=section_ids
        ).values_list('rule_id', flat=True)))


class Section(models.Model):
    book = models.ForeignKey('books.Book')
    order = models.IntegerField(default=0)
    title = models.CharField(max_length=125, null=True, blank=True)
    slug = models.SlugField(max_length=125, unique=True, default='')
    content = models.TextField(default='', blank=True)
    rules = models.ManyToManyField('rules.Rule', through='books.SectionRule')

    class Meta:
        ordering = ['order', ]

    def __str__(self):
        return '{}: {}'.format(self.book, self.title)


class SectionRule(models.Model):
    section = models.ForeignKey('books.Section')
    rule = models.ForeignKey('rules.Rule')
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order', ]

    def __str__(self):
        return '{}: {}'.format(self.section, self.rule)
