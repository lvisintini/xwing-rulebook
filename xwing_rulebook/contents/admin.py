import os

from django import forms
from django.conf import settings
from django.contrib import admin
from django.db import models
from django.utils.safestring import mark_safe

from contents.models import Content, TextContent, ImageContent, Image, Link

from polymorphic.admin import (
    PolymorphicParentModelAdmin, PolymorphicChildModelAdmin, PolymorphicChildModelFilter
)


class LinkInline(admin.StackedInline):
    model = Link
    extra = 0


class ImageAdminForm(forms.ModelForm):
    file = forms.ChoiceField(required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        choices = []

        for dir_path, _, filenames in os.walk(os.path.join(settings.STATICFILES_DIRS[0], 'images')):

            choices.extend([
                (os.path.join(dir_path, f).replace(settings.STATICFILES_DIRS[0], ''), ) * 2
                for f in filenames if f.endswith('.png')
            ])

        self.fields['file'].choices = sorted(choices)


class TextContentAdminForm(forms.ModelForm):
    def has_changed(self):
        return True

    def clean(self):
        cleaned_data = super().clean()
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
class ContentAdmin(PolymorphicParentModelAdmin):
    base_model = Content
    child_models = (TextContent, ImageContent)
    list_display = (
        'id', 'polymorphic_type', 'title', '__str__', 'linked_clause_count', 'related_rules',
        'source', 'page'
    )
    search_fields = ['id', 'textcontent__content', 'imagecontent__image__alt_text']
    readonly_fields = ('linked_clause_count', 'related_rules')
    list_filter = [PolymorphicChildModelFilter, ClauseCountFilter, 'source']

    def linked_clause_count(self, obj):
        return obj.clause_count
    linked_clause_count.admin_order_field = 'clause_count'

    def polymorphic_type(self, obj):
        return obj.polymorphic_ctype.name.replace(' content', '')
    polymorphic_type.short_description = 'type'
    polymorphic_type.admin_order_field = 'polymorphic_ctype'

    def related_rules(self, obj):
        return ', '.join(obj.clause_set.values_list('rule__name', flat=True))

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.annotate(clause_count=models.Count('clause', distinct=True))
        return qs


@admin.register(TextContent)
class TextContentAdmin(PolymorphicChildModelAdmin):
    base_model = Content
    base_form = TextContentAdminForm
    inlines = (LinkInline, )


@admin.register(ImageContent)
class ImageContentAdmin(PolymorphicChildModelAdmin):
    base_model = Content
    readonly_fields = ('render_image', )

    def render_image(self, obj):
        if obj.image:
            return mark_safe("<br/><img src={static_url} />".format(
                static_url=obj.image.static_url)
            )
        return None
    render_image.short_description = 'Preview'


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'caption', 'alt_text')
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
