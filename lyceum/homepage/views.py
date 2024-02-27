from http import HTTPStatus

from django.http import HttpResponse
from django.shortcuts import render

__all__ = ["coffee", "home"]


def home(request):
    template = "homepage/index.html"
    context = {}
    return render(request, template, context)


def coffee(request):
    return HttpResponse("Я чайник", status=HTTPStatus.IM_A_TEAPOT)
