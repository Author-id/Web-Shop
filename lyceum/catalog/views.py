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
        "catalog/catalog.html",
        {"items": items},
    )


def item_detail(request: HttpResponse, pk: int) -> HttpResponse:
    template = "catalog/catalog_pk.html"
    item = django.shortcuts.get_object_or_404(
        catalog.models.Item.objects.published()
    )
    context = {
        "item": item,
    }
    return django.shortcuts.render(request, template, context)


def extract_number(request: HttpResponse, number: int) -> HttpResponse:
    return HttpResponse(number)
