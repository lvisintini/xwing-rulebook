from django import forms
from django.contrib import admin
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
        if not self.cleaned_data.get('format', {}).get('keep_line_breaks', False):
            return ' '.join(self.cleaned_data['text'].strip().splitlines())
        return self.cleaned_data['text'].strip()

    def clean_format(self):
        format_data = self.cleaned_data['format']

        if format_data.get('type') not in ['text', 'item:ul', 'item:ol', 'table']:
            raise forms.ValidationError('Invalid format["type"]')

        if not isinstance(format_data.get('level'), int):
            raise forms.ValidationError('Invalid format["level"]')

        if not isinstance(format_data.get('expansion_rule', False), bool):
            raise forms.ValidationError('Invalid format["expansion_rule"]')

        if not isinstance(format_data.get('keep_line_breaks', False), bool):
            raise forms.ValidationError('Invalid format["keep_line_breaks"]')

        return format_data


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
    list_display = ('id', 'name', )
    inlines = (ParagraphInline, )
    form = RuleAdminForm
    sortable_field_name = 'id'


class RuleBookRuleInline(nested_admin.NestedTabularInline):
    model = models.RuleBookRule
    sortable_field_name = 'order'
    extra = 0


@admin.register(models.RuleBook)
class RuleBookAdmin(nested_admin.NestedModelAdmin):
    list_display = ('name', 'code', 'version')
    inlines = (RuleBookRuleInline, )


class ReferenceInline(admin.TabularInline):
    model = models.Reference
    extra = 0


@admin.register(models.Paragraph)
class ParagraphAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'needs_revision')
    inlines = (ReferenceInline, )
    list_filter = ['needs_revision', ]
    search_fields = ['text', ]
    form = ParagraphAdminForm
