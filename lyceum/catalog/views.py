from django.http import HttpResponse
import django.shortcuts

import catalog.models

__all__ = [
    "item_list",
    "item_detail",
    "extract_number",
]


def item_list(request: HttpResponse) -> HttpResponse:
    items = catalog.models.Item.objects.published()
    return django.shortcuts.render(
        request,
        "catalog/item_list.html",
        {"items": items},
    )


def item_detail(request: HttpResponse, pk: int) -> HttpResponse:
    item = django.shortcuts.get_object_or_404(
        catalog.models.Item.objects.filter(
            category__is_published=True,
            is_published=True,
        )
        .select_related("category", "main_image")
        .prefetch_related(
            django.db.models.Prefetch(
                "tags",
                queryset=catalog.models.Tag.objects.filter(
                    is_published=True,
                ).only("name"),
            ),
            "images",
        )
        .only(
            "name",
            "category__name",
            "text",
            "main_image__image",
            "tags__name",
            "images__image",
        ),
        pk=pk,
    )
    return django.shortcuts.render(
        request,
        "catalog/item_detail.html",
        {"item": item},
    )


def extract_number(request: HttpResponse, number: int) -> HttpResponse:
    return HttpResponse(number)
