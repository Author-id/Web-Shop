from http import HTTPStatus

from django.http import HttpResponse
from django.shortcuts import render

__all__ = ["home", "teapot"]


def home(request):
    return render(request, "homepage/index.html")


def teapot(request):
    return HttpResponse("Я чайник", status=HTTPStatus.IM_A_TEAPOT)
