from django import forms
from django.contrib import admin
from django.db import models
from django.utils.safestring import mark_safe

from contents.models import Content, TextContent, ImageContent, Image

from polymorphic.admin import PolymorphicParentModelAdmin, PolymorphicChildModelAdmin, PolymorphicChildModelFilter


class TextContentAdminForm(forms.ModelForm):
    def has_changed(self):
        return True

    def clean(self):
        cleaned_data = super().clean()
        if not cleaned_data.get('keep_line_breaks', False):
            cleaned_data['content'] = ' '.join(cleaned_data['content'].strip().splitlines())
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


@admin.register(ImageContent)
class ImageContentAdmin(PolymorphicChildModelAdmin):
    base_model = Content


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

    def render_image(self, obj):
        if obj.file:
            return mark_safe("<br/><img src={static_url} />".format(static_url=obj.static_url))
        return None
    render_image.short_description = 'Image'
