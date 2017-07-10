import json

from django.db import models
from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.utils.html import escape

from integrations.models import Product, Ship, Pilot, Upgrade, DamageDeck, Condition
from rules.constants import SOURCE_TYPES


class SourceCountFilter(admin.SimpleListFilter):
    title = "Source Count"
    parameter_name = "source_count"

    def lookups(self, request, model_admin):
        return (
            ('0', '0 sources'),
            ('1', '1 sources'),
            ('2+', '2+ sources'),
        )

    def queryset(self, request, queryset):
        if self.value() == '0':
            return queryset.filter(source_count=0)
        if self.value() == '1':
            return queryset.filter(source_count=1)
        if self.value() == '2+':
            return queryset.filter(source_count__gte=2)
        return queryset


class ModelWithJSON(admin.ModelAdmin):
    list_display = ('name', 'id')
    search_fields = ['name', ]
    readonly_fields = ['data', 'display_data', 'id']
    save_on_top = True

    def display_data(self, obj):
        return mark_safe("<br/><pre>{}</pre>".format(escape(json.dumps(obj.data, indent=2))))
    display_data.short_description = 'Data'

    def get_fieldsets(self, request, obj=None):
        fieldsets = super().get_fieldsets(request, obj)
        fieldsets[0][1]['fields'].remove('data')
        fieldsets[0][1]['fields'].remove('id')
        fieldsets[0][1]['fields'].insert(0, 'id')
        return fieldsets


@admin.register(Product)
class ProductAdmin(ModelWithJSON):
    list_display = ('name', 'sku', 'release_date', 'sources_display', 'source_count')
    search_fields = ['name', 'sku']
    readonly_fields = ['data', 'display_data', 'source_count', 'sources_display', 'id']
    filter_horizontal = ['sources', ]
    list_filter = [SourceCountFilter, ]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.annotate(source_count=models.Count('sources'))
        return qs

    def source_count(self, obj):
        return obj.source_count
    source_count.admin_order_field = 'source_count'

    def sources_display(self, obj):
        return mark_safe('<br/>'.join([
            "<a href={}>{}</a>".format(
                reverse('admin:rules_source_change', args=[s.id, ]),
                '[{}] {} {}'.format(s, s.name, dict(SOURCE_TYPES.as_choices)[s.type])
            )
            for s in obj.sources.all()
        ]))
    sources_display.short_description = 'Sources'


@admin.register(Ship)
class ShipAdmin(ModelWithJSON):
    pass


@admin.register(Pilot)
class PilotAdmin(ModelWithJSON):
    pass


@admin.register(Upgrade)
class UpgradeAdmin(ModelWithJSON):
    pass


@admin.register(Condition)
class ConditionAdmin(ModelWithJSON):
    pass


@admin.register(DamageDeck)
class DamageDeckAdmin(ModelWithJSON):
    list_display = ('name', 'type')
    search_fields = ['name', 'type']
