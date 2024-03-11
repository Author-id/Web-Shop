from django.urls import path

from homepage import views

app_name = "homepage"
urlpatterns = [
    path("", views.home, name="main"),
    path("coffee/", views.coffee, name="coffee"),
    path("echo/", views.echo, name="echo"),
    path("echo/submit/", views.echo, name="echo_submit"),
]
