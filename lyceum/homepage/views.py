from http import HTTPStatus

from django.http import HttpResponse
from django.shortcuts import render

__all__ = ["coffee", "home"]


def home(request):
    template = "homepage/index.html"
    return render(request, template)


def coffee(request):
    return HttpResponse("Я чайник", status=HTTPStatus.IM_A_TEAPOT)
