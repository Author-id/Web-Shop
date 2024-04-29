import datetime
import random

from django.db.models import Count, F, Sum
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
import django.views.generic

import catalog.models
from rating.forms import DeleteRatingForm, RatingForm
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


class ItemDetailView(django.views.generic.DetailView):
    template_name = "catalog/item_detail.html"
    context_object_name = "item"
    queryset = catalog.models.Item.objects.published()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        item = self.get_object()
        ratings = Rating.objects.filter(item=item).aggregate(
            sum=Sum("rating"),
            count=Count("rating"),
        )
        rating_count = ratings["count"]
        rating_sum = ratings["sum"] or 0

        user_rating = None
        if self.request.user.is_authenticated:
            user_rating = Rating.objects.filter(
                user=self.request.user,
                item=item,
            ).first()

        context.update(
            {
                "rating_form": RatingForm(instance=user_rating),
                "delete_rating_form": DeleteRatingForm(),
                "rating": (
                    round(rating_sum / rating_count, 2)
                    if rating_count > 0
                    else 0
                ),
                "rating_count": rating_count,
                "user_rating": user_rating,
            },
        )

        return context

    def post(self, request: HttpRequest, pk: int) -> HttpResponse:
        self.object = self.get_object()
        context = self.get_context_data()
        user_rating = context["user_rating"]
        form = RatingForm(request.POST, instance=user_rating)
        delete_form = DeleteRatingForm(request.POST)
        context["rating_form"] = form
        if self.request.user.is_authenticated:
            if form.is_valid():
                if user_rating:
                    form.save()
                else:
                    user_rating = form.save(False)
                    user_rating.user = self.request.user
                    user_rating.item = self.object
                    user_rating.save()

                return redirect(reverse("catalog:item_detail", args=[pk]))

            if user_rating and delete_form.is_valid():
                user_rating.delete()
                return redirect(reverse("catalog:item_detail", args=[pk]))

        return self.render_to_response(context)


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
