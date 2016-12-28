from django import forms
from django.contrib import admin
from django.forms import formset_factory
import nested_admin

from rule import models


@admin.register(models.Source)
class SourceAdmin(admin.ModelAdmin):
    list_display = ('name', 'date', 'version')


class ReferenceInline(nested_admin.NestedTabularInline):
    model = models.Reference
    extra = 0


class ParagraphAdminForm(forms.ModelForm):

    def has_changed(self):
        return True

    def clean_text(self):
        return ' '.join(self.cleaned_data['text'].strip().splitlines())


class ParagraphInline(nested_admin.NestedTabularInline):
    model = models.Paragraph
    form = ParagraphAdminForm
    inlines = (ReferenceInline, )
    sortable_field_name = 'order'
    extra = 0


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
    extra = 0


@admin.register(models.RuleBook)
class RuleBookAdmin(nested_admin.NestedModelAdmin):
    list_display = ('name', 'version')
    inlines = (RuleBookRuleInline, )
