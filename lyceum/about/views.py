from django.shortcuts import render

__all__ = ["description"]


def description(request):
    template = "about/description.html"
    return render(request, template)
