from django import forms
from django.contrib import admin
from django.db import models
import nested_admin

from rule.models import (
    BookSection, Clause, ClauseContent, ClauseContentVersion, SectionRule, Source, Rule, RuleBook
)


class ClauseContentAdminForm(forms.ModelForm):
    def has_changed(self):
        return True

    def clean_content(self):
        if not self.cleaned_data.get('keep_line_breaks', False):
            return ' '.join(self.cleaned_data['content'].strip().splitlines())
        return self.cleaned_data['content'].strip()


class RuleAdminForm(forms.ModelForm):
    def clean_name(self):
        return self.cleaned_data['name'].capitalize()


class ClauseContentVersionInline(nested_admin.NestedTabularInline):
    fields = ('content', 'content_related_rules', 'active', )
    model = ClauseContentVersion
    extra = 0
    readonly_fields = ['content_related_rules',]
    raw_id_fields = ['content', ]

    def content_related_rules(self, obj):
        if obj.content:
            return ', '.join(obj.content.clause_set.values_list('rule__name', flat=True))
        return ''


class ClauseInline(nested_admin.NestedTabularInline):
    model = Clause
    inlines = (ClauseContentVersionInline, )
    sortable_field_name = 'order'
    extra = 0


class ClauseContentInline(nested_admin.NestedTabularInline):
    model = ClauseContent
    extra = 0
    form = ClauseContentAdminForm


class SectionRuleInline(nested_admin.NestedTabularInline):
    model = SectionRule
    sortable_field_name = 'order'
    extra = 0


class BookSectionInline(nested_admin.NestedTabularInline):
    model = BookSection
    sortable_field_name = 'order'
    inlines = (SectionRuleInline, )
    extra = 0


@admin.register(Source)
class SourceAdmin(admin.ModelAdmin):
    list_display = ('name', 'date', 'version')


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


@admin.register(ClauseContent)
class ClauseContentAdmin(admin.ModelAdmin):
    list_display = ('id', '__str__', 'linked_clause_count', 'related_rules')
    form = ClauseContentAdminForm
    search_fields = ['id', 'content']
    readonly_fields = ('linked_clause_count', 'related_rules')
    list_filter = [ClauseCountFilter, ]

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
class RuleAdmin(nested_admin.NestedModelAdmin):
    list_display = ('name', 'id',)
    inlines = (ClauseInline, )
    form = RuleAdminForm
    sortable_field_name = 'id'
    filter_horizontal = ['related_topics', ]
    save_on_top = True
    search_fields = ['name', ]


@admin.register(RuleBook)
class RuleBookAdmin(nested_admin.NestedModelAdmin):
    list_display = ('name', 'code', 'version')
    inlines = (BookSectionInline, )


@admin.register(Clause)
class ClauseAdmin(nested_admin.NestedModelAdmin):
    list_display = ('__str__', 'needs_revision')
    list_filter = ['needs_revision', ]
    inlines = (ClauseContentVersionInline, )
