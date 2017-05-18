from collections import defaultdict

from django import forms
from django.contrib import admin
from django.utils.safestring import mark_safe
from django.template.defaultfilters import escape

from faqs.models import Faq
from faqs.constants import TOPICS
from utils.lib import word_sensitive_grouper


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
    list_display = (
        'id', 'display_topic', 'order', 'display_text', 'display_rules', 'source', 'page'
    )
    search_fields = ['question', 'answer']
    list_filter = ['topic', ]
    form = FaqAdminForm
    raw_id_fields = ['related_clauses', ]
    readonly_fields = ['display_rules', 'display_text', 'display_topic']
    filter_horizontal = ['related_rules', ]

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
                'related_rules',
                'display_rules',
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
        related = defaultdict(list)
        for rule in obj.related_rules.all():
            related[str(rule)] = []

        for clause in obj.related_clauses.all():
            related[str(clause.rule)].append(str(clause.id))

        verbose_related = [
            '{}{}'.format(rule_name, ' <sup>{}</sup>'.format(', '.join(clauses)) if clauses else '')
            for rule_name, clauses in related.items()
        ]

        return mark_safe('<br/>'.join(verbose_related))
    display_rules.short_description = 'Rules'

    def display_text(self, obj):
        return mark_safe("<strong>Q:</strong> {}<br/><br/><strong>A:</strong> {}".format(
            '<br/>'.join(word_sensitive_grouper(escape(obj.question), 100)),
            '<br/>'.join(word_sensitive_grouper(escape(obj.answer), 100)),

        ))
    display_text.short_description = 'FAQ'

    def display_topic(self, obj):
        return dict(TOPICS.as_choices)[obj.topic]
    display_topic.short_description = 'Topic'
    display_topic.admin_order_field = 'topic_order'
