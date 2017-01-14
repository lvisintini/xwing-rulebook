from django.db import models
from django.conf import settings

from utils.lib import render_template


CLAUSE_TYPES = (
    ('text', 'Text'),
    ('item:ul', 'Unordered Item'),
    ('item:ol', 'Ordered Item'),
    ('image', 'Image'),
    ('table', 'Table'),
)

SOURCE_TYPES = (
    ('M', 'Manual'),
    ('RC', 'Reference Card'),
    ('RR', 'Rules Reference'),
    ('FAQ', 'FAQ'),
)

SOURCE_TYPE_PRECEDENCE = {
    'FAQ': 0,
    'RR': 1,
    'RC': 2,
    'M': 3,
    'OTHER': 5,
}


class Source(models.Model):
    name = models.CharField(max_length=125)
    date = models.DateField(blank=True, null=True)
    code = models.CharField(max_length=50, default='', unique=True)
    type = models.CharField(max_length=50, choices=SOURCE_TYPES, default='RC')
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
            'book': rulebook,
            'section': section,
        }
        return render_template('rule.md', context).strip()

    def __str__(self):
        return self.name


class Clause(models.Model):
    rule = models.ForeignKey('rules.Rule', related_name='clauses')
    order = models.IntegerField(default=0)
    type = models.CharField(max_length=10, choices=CLAUSE_TYPES, default='item:ul')
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
                    models.When(content__source__type='FAQ', then=SOURCE_TYPE_PRECEDENCE['FAQ']),
                    models.When(content__source__type='RR', then=SOURCE_TYPE_PRECEDENCE['RR']),
                    models.When(content__source__type='RC', then=SOURCE_TYPE_PRECEDENCE['RC']),
                    models.When(content__source__type='M', then=SOURCE_TYPE_PRECEDENCE['M']),
                    default=SOURCE_TYPE_PRECEDENCE['OTHER'],
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
