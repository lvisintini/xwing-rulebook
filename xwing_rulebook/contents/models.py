from django.conf import settings
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.db import models
from polymorphic.models import PolymorphicModel


class Content(PolymorphicModel):
    title = models.CharField(max_length=125, null=True, blank=True)
    source = models.ForeignKey('rules.Source', related_name="contents")
    page = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.get_real_instance().__str__()


class TextContent(Content):
    content = models.TextField(default='')
    keep_line_breaks = models.BooleanField(default=False)
    image = models.ForeignKey('contents.Image', blank=True, null=True,
                              related_name='text_contents')

    def __str__(self):
        reference = str(self.source)
        if self.page is not None:
            reference = '{} (Page {})'.format(reference, self.page)

        if self.title:
            return '{} - {}: {}'.format(reference, self.title, self.content)[:125]
        return '{} - {}'.format(reference, self.content)

    class Meta:
        verbose_name = 'Text content'
        verbose_name_plural = 'Text contents'


class ImageContent(Content):
    image = models.ForeignKey('contents.Image', related_name='image_contents')

    def __str__(self):
        reference = str(self.source)
        if self.page is not None:
            reference = '{} (Page {})'.format(reference, self.page)

        if self.title:
            return '{} - {}: {}'.format(reference, self.title, self.image.static_url)
        return '{} - {}'.format(reference, self.image.static_url)

    class Meta:
        verbose_name = 'Image content'
        verbose_name_plural = 'Image contents'


class Image(models.Model):
    caption = models.CharField(max_length=250, default='', blank=True)
    alt_text = models.CharField(max_length=250, default='', blank=True)
    file = models.FilePathField(
        max_length=255,
        path=settings.STATICFILES_DIRS[0],
        recursive=True,
        allow_folders=False,
        null=True,
        blank=True
    )

    @property
    def static_url(self):
        return static(self.file.replace(settings.STATICFILES_DIRS[0], ''))

    def __str__(self):
        return self.static_url
