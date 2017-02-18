from django.contrib import admin
from django.utils.safestring import mark_safe

from integrations.models import Product, Ship, Pilot, Upgrade, DamageDeck


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'sku', 'release_date')
    search_fields = ['name', 'sku']
    readonly_fields = ['json', ]
    filter_horizontal = ['sources', ]
    save_on_top = True

    def json(self, obj):
        return mark_safe("<br/><pre>{}</pre>".format(obj.json))


class ModelWithJSON(admin.ModelAdmin):
    list_display = ('name', 'id')
    search_fields = ['name', ]
    readonly_fields = ['json', ]
    save_on_top = True

    def json(self, obj):
        return mark_safe("<br/><pre>{}</pre>".format(obj.json))


@admin.register(Ship)
class ShipAdmin(ModelWithJSON):
    pass


@admin.register(Pilot)
class PilotAdmin(ModelWithJSON):
    pass


@admin.register(Upgrade)
class UpgradeAdmin(ModelWithJSON):
    pass


@admin.register(DamageDeck)
class DamageDeckAdmin(ModelWithJSON):
    list_display = ('name', 'type')
    search_fields = ['name', 'type']
