from django import forms
from django.contrib import admin
import nested_admin

from rule import models


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
    model = models.ClauseContentVersion
    extra = 0
    raw_id_fields = ['content', ]


class ClauseInline(nested_admin.NestedTabularInline):
    model = models.Clause
    inlines = (ClauseContentVersionInline, )
    sortable_field_name = 'order'
    extra = 0


class ClauseContentInline(nested_admin.NestedTabularInline):
    model = models.ClauseContent
    extra = 0
    form = ClauseContentAdminForm


class SectionRuleInline(nested_admin.NestedTabularInline):
    model = models.SectionRule
    sortable_field_name = 'order'
    extra = 0


class BookSectionInline(nested_admin.NestedTabularInline):
    model = models.BookSection
    sortable_field_name = 'order'
    inlines = (SectionRuleInline, )
    extra = 0


@admin.register(models.Source)
class SourceAdmin(admin.ModelAdmin):
    list_display = ('name', 'date', 'version')


@admin.register(models.ClauseContent)
class ClauseContentAdmin(nested_admin.NestedModelAdmin):
    list_display = ('id', '__str__')
    form = ClauseContentAdminForm
    search_fields = ['id', 'content']


@admin.register(models.Rule)
class RuleAdmin(nested_admin.NestedModelAdmin):
    list_display = ('name', 'id',)
    inlines = (ClauseInline, )
    form = RuleAdminForm
    sortable_field_name = 'id'
    filter_horizontal = ['related_topics', ]
    save_on_top = True


@admin.register(models.RuleBook)
class RuleBookAdmin(nested_admin.NestedModelAdmin):
    list_display = ('name', 'code', 'version')
    inlines = (BookSectionInline, )


@admin.register(models.Clause)
class ClauseAdmin(nested_admin.NestedModelAdmin):
    list_display = ('__str__', 'needs_revision')
    list_filter = ['needs_revision', ]
    inlines = (ClauseContentVersionInline, )
