from django.contrib import admin
from sorl.thumbnail.admin import AdminImageMixin

import catalog.models

__all__ = []


class ItemMainImageInline(AdminImageMixin, admin.TabularInline):
    model = catalog.models.ItemMainImage


class ItemSecondaryImageInline(AdminImageMixin, admin.TabularInline):
    model = catalog.models.ItemSecondaryImage


@admin.register(catalog.models.Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = (catalog.models.Tag.name.field.name,)


@admin.register(catalog.models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (catalog.models.Category.name.field.name,)


@admin.register(catalog.models.Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = (
        catalog.models.Item.name.field.name,
        catalog.models.Item.is_published.field.name,
    )
    list_editable = (catalog.models.Item.is_published.field.name,)
    list_display_links = (catalog.models.Item.name.field.name,)
    filter_horizontal = (catalog.models.Item.tags.field.name,)

    inlines = [
        ItemMainImageInline,
        ItemSecondaryImageInline,
    ]


@admin.register(catalog.models.ItemMainImage)
class ItemMainImageAdmin(admin.ModelAdmin):
    list_display = (
        catalog.models.ItemMainImage.image_tmb.field_name,
        catalog.models.ItemMainImage.item.field.name,
    )


@admin.register(catalog.models.ItemSecondaryImage)
class ItemSecondaryImageAdmin(admin.ModelAdmin):
    list_display = (
        catalog.models.ItemSecondaryImage.image_tmb.field_name,
        catalog.models.ItemSecondaryImage.item.field.name,
    )
