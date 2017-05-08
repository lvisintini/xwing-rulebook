from django import forms
from django.contrib import admin

from faqs.models import Faq


class FaqAdminForm(forms.ModelForm):
    def has_changed(self):
        return True

    def clean(self):
        cleaned_data = super().clean()
        cleaned_data['question'] = ' '.join(cleaned_data['question'].strip().splitlines())
        cleaned_data['answer'] = ' '.join(cleaned_data['answer'].strip().splitlines())
        return cleaned_data


@admin.register(Faq)
class FaqAdmin(admin.ModelAdmin):
    list_display = ('topic', 'question', 'answer')
    search_fields = ['question', 'answer']
    ordering = ('order', )
    list_filter = ['topic', ]
    form = FaqAdminForm

    readonly_fields = []

    def clauses(self, obj):
        if obj.content:
            return ', '.join(obj.related_clauses.values_list('rule__name', flat=True).disctint())
        return ''