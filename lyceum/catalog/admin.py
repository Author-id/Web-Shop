from django.contrib import admin
from sorl.thumbnail.admin import AdminImageMixin

import catalog.models

__all__ = ["CategoryAdmin", "ItemAdmin", "TagAdmin"]


@admin.register(catalog.models.Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = (catalog.models.Tag.name.__dict__["field"].name,)


@admin.register(catalog.models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (catalog.models.Category.name.__dict__["field"].name,)


class MainImageInline(AdminImageMixin, admin.TabularInline):
    model = catalog.models.MainImage


class ImagesInLine(AdminImageMixin, admin.TabularInline):
    model = catalog.models.Images


@admin.register(catalog.models.Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = (
        catalog.models.Item.name.__dict__["field"].name,
        catalog.models.Item.is_published.__dict__["field"].name,
    )
    list_editable = (catalog.models.Item.is_published.__dict__["field"].name,)
    list_display_links = (catalog.models.Item.name.__dict__["field"].name,)
    filter_horizontal = (catalog.models.Item.tags.__dict__["field"].name,)
    inlines = [
        MainImageInline,
        ImagesInLine,
    ]


@admin.register(catalog.models.MainImage)
class MainImageAdmin(admin.ModelAdmin):
    list_display = (
        catalog.models.MainImage.image_tmb.field_name,
        catalog.models.MainImage.item.field.name,
    )


@admin.register(catalog.models.Images)
class ItemSecondaryImageAdmin(admin.ModelAdmin):
    list_display = (
        catalog.models.Images.image_tmb.field_name,
        catalog.models.Images.item.field.name,
    )
