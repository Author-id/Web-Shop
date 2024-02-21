from django.urls import path

from homepage.views import coffee, home

urlpatterns = [
    path("", home),
    path("coffee/", coffee),
]
