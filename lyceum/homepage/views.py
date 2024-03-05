from django.http import HttpResponse
from django.shortcuts import render

import catalog.models

__all__ = ["home", "coffee"]


def home(request: HttpResponse) -> HttpResponse:
    items = catalog.models.Item.objects.on_main()
    return render(request, "homepage/home.html", {"items": items})


def coffee(request: HttpResponse) -> HttpResponse:
    return HttpResponse("Я чайник", status=418)
