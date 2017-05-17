from django.contrib.staticfiles.templatetags.staticfiles import static
from django.db import models

from contents.constants import CONTENT_TYPES


class Content(models.Model):
    type = models.CharField(max_length=5, default=CONTENT_TYPES.TEXT,
                            choices=CONTENT_TYPES.as_choices)
    title = models.CharField(max_length=125, null=True, blank=True)
    preserve_title_case = models.BooleanField(default=False)
    source = models.ForeignKey('rules.Source', related_name="contents")
    page = models.IntegerField(null=True, blank=True)
    content = models.TextField(default='')
    content_as_per_source = models.TextField(
        default='',
        help_text="If the text in the content field is not a verbatim copy of the source's text, "
                  "Add the original text here.",
        blank=True
    )
    keep_line_breaks = models.BooleanField(default=False)
    image = models.ForeignKey('contents.Image', blank=True, null=True, related_name='contents')

    def __str__(self):
        reference = str(self.source)
        if self.page is not None:
            reference = '{} (Page {})'.format(reference, self.page)

        return '[{}] {}'.format(dict(CONTENT_TYPES.as_choices)[self.type], reference)


class Image(models.Model):
    caption = models.CharField(max_length=250, default='', blank=True)
    alt_text = models.CharField(max_length=250, default='', blank=True)
    file = models.CharField(max_length=255)

    @property
    def static_url(self):
        return static(self.file)

    def __str__(self):
        return self.static_url


class Link(models.Model):
    rule = models.ForeignKey('rules.Rule', blank=True, null=True)
    alias = models.CharField(
        max_length=50,
        unique=True,
        help_text="Used as the link identifier. Use <LINK:{alias}> in your markdown"
    )
    text = models.CharField(
        max_length=255, blank=True, default='',
        help_text="Only used if no rule is provided"
    )
    url = models.CharField(
        max_length=255, blank=True, default='',
        help_text="Used only if no rule is provided."
    )

    def __str__(self):
        return self.alias
