from django.contrib import admin

from catalog import models


@admin.register(models.Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "is_published",
    )
    list_editable = ("is_published",)

    list_display_links = ("name",)

    filter_horizontal = ("tags",)


@admin.register(models.Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "is_published",
    )
    list_editable = ("is_published",)

    list_display_links = ("name",)


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "is_published",
        "weight",
    )
    list_editable = ("is_published",)

    list_display_links = ("name",)
