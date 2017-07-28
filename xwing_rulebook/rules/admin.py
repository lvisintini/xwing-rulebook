import os
from itertools import chain

from django import forms
from django.contrib import admin
from django.conf import settings
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe
from django.template.defaultfilters import escape
from nested_admin import NestedTabularInline, NestedModelAdmin

from contents.constants import CONTENT_TYPES
from rules.models import Clause, ClauseContent, Rule, Source
from rules.constants import RULE_TYPES, CARD_TYPES
from utils.lib import word_sensitive_grouper


class RuleAdminForm(forms.ModelForm):
    def clean(self):
        cleaned_data = super().clean()

        if cleaned_data['type'] != RULE_TYPES.CARD:
            if cleaned_data['card_type'] != CARD_TYPES.NOT_APPLICABLE:
                self.add_error(
                    'card_type', forms.ValidationError(
                        "If rule.type != RULE_TYPES.CARD, rule.card_type needs to be "
                        "CARD_TYPES.NOT_APPLICABLE."
                    )
                )
        else:
            if cleaned_data['card_type'] == CARD_TYPES.NOT_APPLICABLE:
                self.add_error(
                    'card_type', forms.ValidationError(
                        "If rule.type == RULE_TYPES.CARD, rule.card_type needs to be anything "
                        "but CARD_TYPES.NOT_APPLICABLE."
                    )
                )

        if not cleaned_data.get('preserve_name_case', False):
            cleaned_data['name'] = cleaned_data['name'].capitalize()
        return cleaned_data


class ClauseContentInline(NestedTabularInline):
    fields = ('content', 'display_content', 'content_related_rules')
    model = ClauseContent
    extra = 0
    readonly_fields = ['content_related_rules', 'display_content']
    raw_id_fields = ['content', ]

    def content_related_rules(self, obj):
        if obj.content:
            return ', '.join(obj.content.clause_set.values_list('rule__name', flat=True))
        return ''

    def display_content(self, obj):
        if obj.content.type == CONTENT_TYPES.TEXT:
            content = '{title}{text}'.format(
                title='' if not obj.content.title else '<strong>{}:</strong> '.format(
                    escape(obj.content.title)
                ),
                text=escape(obj.content.content),
            )
            return mark_safe('<br/>'.join(word_sensitive_grouper(content, 100)))
        elif obj.content.type == CONTENT_TYPES.IMAGE:
            return obj.content.image.file
        return None
    display_content.short_description = 'Preview'


class ClauseInline(NestedTabularInline):
    model = Clause
    inlines = (ClauseContentInline, )
    sortable_field_name = 'order'
    extra = 0


class ContentCountFilter(admin.SimpleListFilter):
    title = "Content count"
    parameter_name = "content_count"

    def lookups(self, request, model_admin):
        return (
            ('0', '0 contents'),
            ('1+', '1+ contents'),

        )

    def queryset(self, request, queryset):
        if self.value() == '0':
            return queryset.filter(content_count=0)
        if self.value() == '1+':
            return queryset.filter(content_count__gte=1)
        return queryset


class SourceAdminForm(forms.ModelForm):
    file = forms.ChoiceField(required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        choices = []

        walker = chain(
            os.walk(os.path.join(settings.STATICFILES_DIRS[0], 'assets')),
            os.walk(os.path.join(settings.STATICFILES_DIRS[0], 'images', 'lib',)),
        )

        for dir_path, _, filenames in walker:
            file_paths = [
                os.path.join(dir_path, f).replace(settings.STATICFILES_DIRS[0], '')
                for f in filenames
            ]

            choices.extend([
                (f, ) * 2
                for f in file_paths
            ])

        if self.instance.file:
            choices.insert(0, (self.instance.file, ) * 2)
        else:
            choices.insert(0, ('', '---'))

        self.fields['file'].choices = sorted(choices)


@admin.register(Source)
class SourceAdmin(admin.ModelAdmin):
    list_display = (
        '__str__',
        'name',
        'type',
        'products_display',
        'release_date',
        'precedence',
        'content_count',
        'status',
        'display_notes',
        'open_file',
    )
    form = SourceAdminForm
    search_fields = ['name', ]
    readonly_fields = ['release_date', 'precedence', 'display_notes', 'products_display', 'content_count', 'open_file']
    list_filter = ('status', 'type', ContentCountFilter)

    def release_date(self, obj):
        return obj.release_date
    release_date.admin_order_field = 'release_date'

    def precedence(self, obj):
        return obj.precedence
    precedence.admin_order_field = 'precedence'

    def display_notes(self, obj):
        return mark_safe('<br/>'.join(word_sensitive_grouper(escape(obj.notes), 50)))
    display_notes.short_description = 'Notes'
    display_notes.admin_order_field = 'notes'

    def products_display(self, obj):
        return mark_safe('<br/>'.join([
            '<a href="{}">{}</a>'.format(reverse('admin:integrations_product_change', args=[p.id, ]), p)
            for p in obj.products.all().order_by('sku')
        ]))
    products_display.short_description = 'Products'

    def open_file(self, obj):
        if obj.file:
            return mark_safe(
                '<a target="_blank" href="{}">{}</a>'.format(obj.static_file, obj.static_file.split('/')[-1])
            )
        return None
    open_file.short_description = 'File'

    def content_count(self, obj):
        if not obj.content_count:
            return obj.content_count

        return mark_safe('<a href="{}?source_id={}">{}</a>'.format(
            reverse('admin:contents_content_changelist'),
            obj.id,
            obj.content_count
        ))
    content_count.admin_order_field = 'content_count'

    def get_queryset(self, request):
        qs = self.model.enriched.get_queryset()
        ordering = self.get_ordering(request)
        if ordering:
            qs = qs.order_by(*ordering)

        return qs


@admin.register(Rule)
class RuleAdmin(NestedModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('id', 'name', 'link_to_rule', 'type', 'card_type', 'cards_display')
    fieldsets = (
        ('Basic', {
            'fields': (
                'name',
                'slug',
                'preserve_name_case',
                'type',
                'card_type',
                'cards_display'
                'additional_keywords',
                'link_to_rule',
                'expansion_rule',
                'huge_ship_rule',
                'related_rules',
                'last_updated'
            )
        }),
    )
    inlines = (ClauseInline, )
    form = RuleAdminForm
    filter_horizontal = ['related_rules', ]
    list_filter = ['type', 'card_type']
    save_on_top = True
    search_fields = ['name', ]
    readonly_fields = ['link_to_rule', 'cards_display', 'last_updated']

    def cards_display(self, obj):
        links = [
            '<a href="{}">[{}] {}</a>'.format(
                reverse('admin:integrations_{}_change'.format(c.__class__.__name__.lower()), args=[c.id]),
                c.__class__.__name__,
                c.name
            )
            for c in obj.cards
        ]
        return mark_safe('<br/>'.join(links))

    def link_to_rule(self, obj):
        if not obj.slug:
            return None
        rule_link = reverse('rules:rule', args=[], kwargs={'rule_slug': obj.slug})
        return mark_safe("<a target='-blank' href='{}'>{}</a>".format(rule_link, obj.slug))
    link_to_rule.short_description = 'Rule link'


@admin.register(Clause)
class ClauseAdmin(NestedModelAdmin):
    list_display = ('id', '__str__', 'needs_revision')
    list_filter = ['needs_revision', 'type', 'group']
    inlines = (ClauseContentInline, )
