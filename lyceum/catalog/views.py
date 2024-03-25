import datetime
import random

from django.db.models import F
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
import django.views.generic

import catalog.models

from django.shortcuts import render, get_object_or_404
from catalog.models import Item
from rating.models import Rating

__all__ = []


class ItemListView(django.views.generic.ListView):
    template_name = "catalog/item_list.html"
    context_object_name = "items"
    queryset = catalog.models.Item.objects.published()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["chapter"] = _("item_list_title")
        return context


class ItemDetailView(django.views.generic.View):
    template_name = "catalog/item_detail.html"
    context_object_name = "item"
    queryset = catalog.models.Item.objects.get_item()

    def get(self, request, pk):
        item = get_object_or_404(Item, pk=pk)
        ratings = Rating.objects.filter(item=item)
        total_ratings = len(ratings)
        avg_rating = 0
        if total_ratings > 0:
            avg_rating = (
                sum(rating.rating for rating in ratings) / total_ratings
            )

        user_rating = None
        if request.user.is_authenticated:
            user_rating = Rating.objects.filter(
                user=request.user, item=item
            ).first()

        context = {
            "item": item,
            "avg_rating": avg_rating,
            "total_ratings": total_ratings,
            "user_rating": user_rating,
        }
        return render(request, self.template_name, context)

    def post(self, request, pk):
        item = get_object_or_404(Item, pk=pk)
        user_rating = Rating.objects.filter(
            user=request.user, item=item
        ).first()

        if user_rating:
            user_rating.rating = request.POST["rating"]
            user_rating.save()
        else:
            Rating.objects.create(
                user=request.user, item=item, rating=request.POST["rating"]
            )

        return self.get(request, pk)


class ItemListNewView(django.views.generic.ListView):
    template_name = "catalog/item_list.html"
    context_object_name = "items"
    model = catalog.models.Item

    def get_queryset(self):
        qs = self.model.objects.published()
        items = list(
            qs.filter(
                created__gt=timezone.now() - datetime.timedelta(hours=24 * 7),
            ).all(),
        )
        ln_items = len(items)
        return sorted(
            random.sample(items, 5 if ln_items >= 5 else ln_items),
            key=lambda item: item.category.name,
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["chapter"] = _("item_list_title")
        return context


class ItemListFridayView(django.views.generic.ListView):
    template_name = "catalog/item_list.html"
    context_object_name = "items"
    model = catalog.models.Item

    def get_queryset(self):
        qs = self.model.objects.published()
        item_category = catalog.models.Item.category.field.name
        category_name = catalog.models.Category.name.field.name
        return reversed(
            qs.filter(updated__week_day=6).order_by(
                f"-{item_category}__{category_name}",
            )[:5],
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["chapter"] = _("item_list_title")
        return context


class ItemListUnverifiedView(django.views.generic.ListView):
    template_name = "catalog/item_list.html"
    context_object_name = "items"
    model = catalog.models.Item

    def get_queryset(self):
        qs = self.model.objects.published()
        return qs.filter(updated=F("created"))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["chapter"] = _("item_list_title")
        return context
