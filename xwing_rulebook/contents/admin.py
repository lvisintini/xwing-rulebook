import os

from django import forms
from django.conf import settings
from django.contrib import admin
from django.db import models
from django.utils.safestring import mark_safe
from django.template.defaultfilters import escape

from contents.models import Content, Image, Link
from rules.models import Source
from contents.constants import CONTENT_TYPES
from utils.lib import word_sensitive_grouper


class ImageAdminForm(forms.ModelForm):
    file = forms.ChoiceField(required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        choices = []

        loaded_images = list(Image.objects.values_list('file', flat=True))

        for dir_path, _, filenames in os.walk(os.path.join(settings.STATICFILES_DIRS[0], 'images')):
            file_paths = [
                os.path.join(dir_path, f).replace(settings.STATICFILES_DIRS[0], '')
                for f in filenames if f.endswith('.png') or f.endswith('.svg')
            ]

            choices.extend([
                (f, ) * 2
                for f in file_paths
                if f not in loaded_images
            ])

        if self.instance.id:
            choices.append((self.instance.file, ) * 2)

        self.fields['file'].choices = sorted(choices)


class ContentAdminForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['source'].queryset = Source.objects.order_by('-status', 'type', 'name')

    def has_changed(self):
        return True

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data['type'] == CONTENT_TYPES.TEXT:
            if not cleaned_data.get('keep_line_breaks', False):
                cleaned_data['content'] = ' '.join(cleaned_data['content'].strip().splitlines())
                cleaned_data['content_as_per_source'] = ' '.join(
                    cleaned_data.get('content_as_per_source', '').strip().splitlines()
                )

        if not cleaned_data.get('preserve_title_case', False):
            cleaned_data['title'] = cleaned_data['title'].capitalize()
        return cleaned_data


class ClauseCountFilter(admin.SimpleListFilter):
    title = "Clause Counts"
    parameter_name = "clause_count"

    def lookups(self, request, model_admin):
        return (
            ('0', '0 clauses'),
            ('1', '1 clause'),
            ('2+', '2+ clauses'),
        )

    def queryset(self, request, queryset):
        if self.value() == '0':
            return queryset.filter(clause_count=0)
        if self.value() == '1':
            return queryset.filter(clause_count=1)
        if self.value() == '2+':
            return queryset.filter(clause_count__gte=2)
        return queryset


@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'type', 'title', 'display_content', 'linked_clause_count', 'related_rules',
        'source', 'page'
    )
    form = ContentAdminForm
    fieldsets = (
        (None, {
            'fields': [
                'type',
                'title',
                'preserve_title_case',
                'source',
                'page',
            ],
        }),
        ('Image', {
            'fields': [
                'image',
                'render_image',
            ],
            'classes': ('collapse',)
        }),
        ('Text', {
            'fields': [
                'content',
                'content_as_per_source',
                'keep_line_breaks',
            ],
            'classes': ('collapse',)
        }),
    )
    search_fields = ['id', 'content', 'image__alt_text']
    readonly_fields = ('linked_clause_count', 'related_rules', 'render_image', 'display_content')
    list_filter = ['type', ClauseCountFilter, 'source']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.annotate(clause_count=models.Count('clause', distinct=True))

        qs = qs.annotate(
            joined_content=models.Case(
                models.When(
                    type=CONTENT_TYPES.TEXT,
                    then='content'
                ),
                default='image__file',
                output_field=models.CharField()
            )
        )
        return qs

    def linked_clause_count(self, obj):
        return obj.clause_count
    linked_clause_count.admin_order_field = 'clause_count'

    def related_rules(self, obj):
        return ', '.join(obj.clause_set.values_list('rule__name', flat=True))

    def render_image(self, obj):
        if obj.image:
            return mark_safe("<br/><img src={static_url} />".format(
                static_url=obj.image.static_url)
            )
        return None
    render_image.short_description = 'Preview'

    def display_content(self, obj):
        if obj.type == CONTENT_TYPES.TEXT:
            return mark_safe('<br/>'.join(word_sensitive_grouper(escape(obj.content), 100)))
        elif obj.type == CONTENT_TYPES.IMAGE:
            return obj.image.file
        return None
    display_content.short_description = 'Content'
    display_content.admin_order_field = 'joined_content'



@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('file', 'caption', 'alt_text')
    readonly_fields = ('render_image', )
    search_fields = ['file', ]
    fieldsets = (
        (None, {
            'fields': (
                'file', 'caption', 'alt_text', 'render_image',
            )
        }),
    )
    form = ImageAdminForm

    def render_image(self, obj):
        if obj.file:
            return mark_safe("<br/><img src={static_url} />".format(static_url=obj.static_url))
        return None
    render_image.short_description = 'Image'


@admin.register(Link)
class LinkAdmin(admin.ModelAdmin):
    list_display = ('alias', 'label', 'target', 'placeholder')
    readonly_fields = ['label', 'target', 'placeholder']

    def label(self, obj):
        return "{label}{expansion_icon}".format(
            label=obj.rule.name if obj.rule else obj.text,
            expansion_icon='†' if obj.rule and obj.rule.expansion_rule else ''
        )

    def target(self, obj):
        return str(obj.rule) if obj.rule else obj.url

    def placeholder(self, obj):
        if obj.id:
            return '<LINK:{}>'.format(obj.alias)
        return '-'
