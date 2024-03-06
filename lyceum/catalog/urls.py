from django.urls import path, re_path, register_converter

from catalog import converters, views


register_converter(converters.PositiveIntegerConverter, "pint")
app_name = "catalog"

urlpatterns = [
    path("", views.item_list, name="main"),
    path("<int:pk>/", views.item_detail, name="item_detail"),
    re_path(r"^re/(?P<pk>[1-9]\d*)/", views.item_detail, name="re"),
    path("converter/<pint:pk>/", views.item_detail, name="converter"),
    path("new/", views.item_new, name="new"),
    path("friday/", views.item_friday, name="friday"),
    path("unverified/", views.item_unverified, name="unverified"),
]
