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
    list_display = ('id', 'topic', 'order', 'question', 'answer', 'display_rules', 'source', 'page')
    search_fields = ['question', 'answer']
    ordering = ('topic', 'order', )
    list_filter = ['topic', ]
    form = FaqAdminForm
    raw_id_fields = ['related_clauses', ]
    readonly_fields = ['display_rules', ]

    fieldsets = (
        (None, {
            'fields': (
                'topic',
                'question',
                'answer',
                'source',
                'page',
                'order',
                'related_clauses',
                'rules',
            )
        }),
        ('Original text', {
            'fields': (
                'question_as_per_source',
                'answer_as_per_source'
            ),
            'classes': ('collapse', )
        }),
    )

    def display_rules(self, obj):
        if obj.related_clauses.count():
            return ', '.join(obj.related_clauses.values_list('rule__name', flat=True).distinct())
        return ''
