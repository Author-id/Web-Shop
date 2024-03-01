from django.urls import path, re_path, register_converter

from catalog import converters, views


register_converter(converters.PositiveIntegerConverter, "pint")
app_name = "catalog"

urlpatterns = [
    path("", views.item_list, name="item-list"),
    path("<int:pk>/", views.item_detail, name="item_detail"),
    re_path(r"^re/(?P<pk>[1-9]\d*)/", views.item_detail, name="re"),
    path("converter/<pint:pk>/", views.item_detail, name="converter"),
]
