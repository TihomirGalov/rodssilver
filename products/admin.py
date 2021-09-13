from django.contrib import admin
from products.models import Category, Item, Image, Variation, ItemVariation
from django.utils.translation import gettext_lazy as _


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'products_total']

    def products_total(self, obj):
        return obj.products.all().count() or 0

    products_total.short_description = _("Total Products")


class ImageAdmin(admin.TabularInline):
    model = Image
    min_num = 1
    extra = 0


class ItemVariation(admin.TabularInline):
    model = ItemVariation
    min_num = 1
    extra = 0


@admin.register(Variation)
class ItemAdmin(admin.ModelAdmin):
    inlines = [ItemVariation,]
    list_display = ['name', 'item']


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    inlines = [ImageAdmin,]
    list_display = ['title', 'price', 'category']
    search_fields = ['title']
