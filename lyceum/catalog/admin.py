from django.contrib import admin

from . import models


@admin.register(models.CatalogItem)
class ItemAdmin(admin.ModelAdmin):

    list_display = (
        models.CatalogCategory.name.field.name,
        models.CatalogCategory.is_published.field.name,
    )
    list_editable = ("is_published",)
    list_display_links = ("name",)
    filter_horizontal = ("tags",)


@admin.register(models.CatalogCategory)
class CatalogAdmin(admin.ModelAdmin):
    list_display = (
        models.CatalogCategory.name.field.name,
        models.CatalogCategory.is_published.field.name,
    )
    list_editable = ("is_published",)
    list_display_links = ("name",)


@admin.register(models.CatalogTag)
class TagAdmin(admin.ModelAdmin):
    list_display = (
        models.CatalogTag.name.field.name,
        models.CatalogTag.is_published.field.name,
    )
    list_editable = ("is_published",)
    list_display_links = ("name",)
