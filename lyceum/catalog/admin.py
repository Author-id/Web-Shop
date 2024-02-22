from django.contrib import admin

import catalog.models


@admin.register(catalog.models.Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = (catalog.models.Tag.name.__dict__["field"].name,)


@admin.register(catalog.models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (catalog.models.Category.name.__dict__["field"].name,)


@admin.register(catalog.models.Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = (
        catalog.models.Item.name.__dict__["field"].name,
        catalog.models.Item.is_published.__dict__["field"].name,
    )
    list_editable = (catalog.models.Item.is_published.__dict__["field"].name,)
    list_display_links = (catalog.models.Item.name.__dict__["field"].name,)
    filter_horizontal = (catalog.models.Item.tags.__dict__["field"].name,)
