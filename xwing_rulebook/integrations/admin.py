from django.contrib import admin
from django.utils.safestring import mark_safe

from integrations.models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'sku', 'release_date')
    search_fields = ['name', 'sku']
    readonly_fields = ['json', ]

    def json(self, obj):
        return mark_safe("<br/><pre>{}</pre>".format(obj.json))