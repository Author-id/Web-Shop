from http import HTTPStatus
from pathlib import Path

from django.conf import settings
from django.http import FileResponse, HttpResponse
from django.shortcuts import render

import catalog.models

__all__ = []


def home(request):
    template = "homepage/index.html"
    items = catalog.models.Item.objects.on_main()
    context = {"items": items}
    return render(request, template, context)


def coffee(request):
    return HttpResponse("Я чайник", status=HTTPStatus.IM_A_TEAPOT)


def download(request, path):
    return FileResponse(
        open(settings.MEDIA_ROOT / Path(path), "rb"),
        as_attachment=True,
    )
