from django.shortcuts import render

__all__ = ["description"]


def description(request):
    return render(request, "about/description.html")
