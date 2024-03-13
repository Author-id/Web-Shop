from http import HTTPStatus

from django.http import HttpResponse, HttpResponseNotAllowed
from django.shortcuts import render
from django.urls import reverse

import catalog.models
import homepage.forms

__all__ = []


def home(request):
    homepage_title = "Главная страница!"
    template = "homepage/index.html"
    items = catalog.models.Item.objects.on_main()
    context = {"items": items}
    return render(request, template, context)


def coffee(request):
    return HttpResponse("Я чайник", status=HTTPStatus.IM_A_TEAPOT)


def echo(request):
    form = homepage.forms.EchoForm(request.POST or None)
    if request.path == reverse("homepage:echo_submit"):
        if request.method == "POST" and form.is_valid():
            return HttpResponse(form.cleaned_data["text"])

        return HttpResponseNotAllowed(permitted_methods=["POST"])

    if request.method == "GET":
        context = {"form": form}
        return render(request, "homepage/echo.html", context)

    return HttpResponseNotAllowed(permitted_methods=["GET"])
