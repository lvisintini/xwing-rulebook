from django import forms
from django.contrib import admin
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.safestring import mark_safe

from nested_admin import NestedTabularInline, NestedModelAdmin

from rules.models import Clause, ClauseContent, Content, Rule, Source, SOURCE_TYPES


class ContentAdminForm(forms.ModelForm):
    def has_changed(self):
        return True

    def clean(self):
        cleaned_data = super().clean()
        if not cleaned_data.get('keep_line_breaks', False):
            cleaned_data['content'] = ' '.join(cleaned_data['content'].strip().splitlines())
        return cleaned_data


class RuleAdminForm(forms.ModelForm):
    def clean_name(self):
        return self.cleaned_data['name'].capitalize()


class ClauseContentInline(NestedTabularInline):
    fields = ('content', 'content_related_rules')
    model = ClauseContent
    extra = 0
    readonly_fields = ['content_related_rules', ]
    raw_id_fields = ['content', ]

    def content_related_rules(self, obj):
        if obj.content:
            return ', '.join(obj.content.clause_set.values_list('rule__name', flat=True))
        return ''


class ClauseInline(NestedTabularInline):
    model = Clause
    inlines = (ClauseContentInline, )
    sortable_field_name = 'order'
    extra = 0


class ContentInline(NestedTabularInline):
    model = Content
    extra = 0
    form = ContentAdminForm


@admin.register(Source)
class SourceAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'name', 'type', 'release_date', 'precedence', 'processed')
    search_fields = ['name', ]
    readonly_fields = ['release_date', 'precedence']

    def release_date(self, obj):
        return obj.release_date
    release_date.admin_order_field = 'release_date'

    def precedence(self, obj):
        return obj.precedence
    precedence.admin_order_field = 'precedence'

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.annotate(
            release_date=models.Case(
                models.When(date=None, then=models.Min('product__release_date', distinct=True)),
                default='date'
            )
        )
        qs = qs.annotate(
            precedence=models.Case(
                models.When(
                    content__source__type=SOURCE_TYPES.FAQ,
                    then=SOURCE_TYPES.PRECEDENCE.index(SOURCE_TYPES.FAQ)
                ),
                models.When(
                    content__source__type=SOURCE_TYPES.RULES_REFERENCE,
                    then=SOURCE_TYPES.PRECEDENCE.index(SOURCE_TYPES.RULES_REFERENCE)
                ),
                models.When(
                    content__source__type=SOURCE_TYPES.REFERENCE_CARD,
                    then=SOURCE_TYPES.PRECEDENCE.index(SOURCE_TYPES.REFERENCE_CARD)
                ),
                models.When(
                    content__source__type=SOURCE_TYPES.MANUAL,
                    then=SOURCE_TYPES.PRECEDENCE.index(SOURCE_TYPES.MANUAL)
                ),
                default=SOURCE_TYPES.PRECEDENCE.index(SOURCE_TYPES.OTHER),
                output_field=models.IntegerField()
            )
        )

        return qs


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
        'id', 'title', '__str__', 'linked_clause_count', 'related_rules', 'source', 'page'
    )
    form = ContentAdminForm
    search_fields = ['id', 'content']
    readonly_fields = ('linked_clause_count', 'related_rules')
    list_filter = [ClauseCountFilter, 'source']

    def linked_clause_count(self, obj):
        return obj.clause_count
    linked_clause_count.admin_order_field = 'clause_count'

    def related_rules(self, obj):
        return ', '.join(obj.clause_set.values_list('rule__name', flat=True))

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.annotate(clause_count=models.Count('clause', distinct=True))
        return qs


@admin.register(Rule)
class RuleAdmin(NestedModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name', 'link_to_rule', 'type')
    inlines = (ClauseInline, )
    form = RuleAdminForm
    sortable_field_name = 'id'
    filter_horizontal = [
        'related_topics', 'related_damage_decks', 'related_upgrades', 'related_pilots'
    ]
    save_on_top = True
    search_fields = ['name', ]
    readonly_fields = ['link_to_rule']

    def link_to_rule(self, obj):
        if not obj.slug:
            return None
        rule_link = reverse('rules:rule', args=[], kwargs={'rule_slug': obj.slug})
        return mark_safe("<a target='-blank' href='{}'>{}</a>".format(rule_link, obj.slug))
    link_to_rule.short_description = 'Rule link'


@admin.register(Clause)
class ClauseAdmin(NestedModelAdmin):
    list_display = ('__str__', 'needs_revision')
    list_filter = ['needs_revision', ]
    inlines = (ClauseContentInline, )
