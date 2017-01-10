from django.contrib import admin
import nested_admin

from books.models import Book, Section, SectionRule


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
