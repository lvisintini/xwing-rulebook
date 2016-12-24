from django import forms
from django.contrib import admin

import nested_admin

from rule import models


@admin.register(models.Source)
class SourceAdmin(admin.ModelAdmin):
    list_display = ('name', 'date', 'version')


class ReferenceInline(nested_admin.NestedTabularInline):
    model = models.Reference
    extra = 1


class ParagraphInline(nested_admin.NestedTabularInline):
    model = models.Paragraph
    inlines = (ReferenceInline, )
    sortable_field_name = 'order'
    extra = 1


class RuleAdminForm(forms.ModelForm):
    def clean_name(self):
        return self.cleaned_data['name'].capitalize()


@admin.register(models.Rule)
class RuleAdmin(nested_admin.NestedModelAdmin):
    list_display = ('name', )
    inlines = (ParagraphInline, )
    form = RuleAdminForm


class RuleBookRuleInline(nested_admin.NestedTabularInline):
    model = models.RuleBookRule
    sortable_field_name = 'order'
    extra = 1


@admin.register(models.RuleBook)
class RuleBookAdmin(nested_admin.NestedModelAdmin):
    list_display = ('name', 'version')
    inlines = (RuleBookRuleInline, )
