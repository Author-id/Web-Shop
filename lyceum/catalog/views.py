from django.http import HttpResponse
from django.shortcuts import render

__all__ = [
    "get_from_converter",
    "get_from_re_path",
    "item_detail",
    "item_list",
]


def item_list(request):
    return render(request, "catalog/item_list.html")


def item_detail(request, pk):
    return render(request, "catalog/item.html")


def get_from_re_path(request, pk):
    return HttpResponse(pk)


def get_from_converter(request, pk):
    return HttpResponse(pk)
