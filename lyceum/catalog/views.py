import datetime
import random

from django.db.models import F
from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

import catalog.models

__all__ = []


def item_list(request):
    template = "catalog/item_list.html"
    items = catalog.models.Item.objects.published().order_by(
        "category__name",
    )
    context = {
        "chapter": _("Список товаров"),
        "items": items,
    }
    return render(request, template, context)


def item_detail(request, pk):
    template = "catalog/item_detail.html"
    item = get_object_or_404(catalog.models.Item.objects.get_item(), pk=pk)
    context = {"item": item}

    return render(request, template, context)


def item_new(request):
    template = "catalog/item_list.html"
    items = list(
        catalog.models.Item.objects.published()
        .filter(created__gt=timezone.now() - datetime.timedelta(hours=24 * 7))
        .all(),
    )
    ln_items = len(items)
    random_items = sorted(
        random.sample(items, 5 if ln_items >= 5 else ln_items),
        key=lambda item: item.category.name,
    )
    context = {
        "chapter": _("Новинки"),
        "items": random_items,
    }
    return render(request, template, context)


def item_friday(request):
    template = "catalog/item_list.html"
    items = reversed(
        catalog.models.Item.objects.published()
        .filter(updated__week_day=6)
        .order_by(
            "-category__name",
        )[:5],
    )
    context = {
        "chapter": _("Пятница"),
        "items": items,
    }
    return render(request, template, context)


def item_unverified(request):
    template = "catalog/item_list.html"
    items = (
        catalog.models.Item.objects.published()
        .filter(updated=F("created"))
        .order_by(
            "category__name",
        )
    )
    context = {
        "chapter": _("Непроверенное"),
        "items": items,
    }
    return render(request, template, context)
