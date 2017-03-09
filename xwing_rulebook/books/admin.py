from django.contrib import admin
from django.utils.safestring import mark_safe
import nested_admin

from books.models import Book, Section, SectionRule
from rules.models import Rule


class SectionRuleInline(nested_admin.NestedTabularInline):
    model = SectionRule
    sortable_field_name = 'order'
    extra = 0


class SectionInline(nested_admin.NestedTabularInline):
    model = Section
    sortable_field_name = 'order'
    inlines = (SectionRuleInline, )
    extra = 0


@admin.register(Book)
class BookAdmin(nested_admin.NestedModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ('name', 'code', 'version')
    inlines = (SectionInline, )
    readonly_fields = ['missing_rules', 'duplicate_rules']

    def missing_rules(self, obj):
        return mark_safe(',<br/>'.join([
            r.name for r in Rule.objects.exclude(id__in=obj.rule_ids)
        ]) or '-')

    def duplicate_rules(self, obj):
        section_ids = obj.section_set.values_list('id', flat=True)
        rule_ids = list(SectionRule.objects.filter(
            section_id__in=section_ids
        ).values_list('rule_id', flat=True))

        dup = [x for x in set(rule_ids) if rule_ids.count(x) > 1]
        return mark_safe(',<br/>'.join([
            r.name for r in Rule.objects.filter(id__in=dup)
        ]) or '-')
