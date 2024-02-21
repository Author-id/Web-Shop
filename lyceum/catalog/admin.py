from django.contrib import admin

from catalog import models


@admin.register(models.Item)
class ItemAdmin(admin.ModelAdmin):

    list_display = (
        models.Category.name.field.name,
        models.Category.is_published.field.name,
    )
    list_editable = ("is_published",)
    list_display_links = ("name",)
    filter_horizontal = ("tags",)


@admin.register(models.Category)
class CatalogAdmin(admin.ModelAdmin):
    list_display = (
        models.Category.name.field.name,
        models.Category.is_published.field.name,
    )
    list_editable = ("is_published",)
    list_display_links = ("name",)


@admin.register(models.Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = (
        models.Tag.name.field.name,
        models.Tag.is_published.field.name,
    )
    list_editable = ("is_published",)
    list_display_links = ("name",)
