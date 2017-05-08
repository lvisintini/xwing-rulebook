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
    list_display = ('topic', 'question', 'answer', 'rules')
    search_fields = ['question', 'answer']
    ordering = ('order', )
    list_filter = ['topic', ]
    form = FaqAdminForm
    raw_id_fields = ['related_clauses', ]
    readonly_fields = ['rules', ]

    def rules(self, obj):
        if obj.related_clauses.count():
            return ', '.join(obj.related_clauses.values_list('rule__name', flat=True,).distinct())
        return ''
