from django.urls import path

from .views import coffee, home

urlpatterns = [
    path("", home),
    path("coffee/", coffee),
]
