from django.http import HttpResponse
from django.shortcuts import render

__all__ = ["description"]


def description(request: HttpResponse) -> HttpResponse:
    return render(request, "about/description.html", {})
