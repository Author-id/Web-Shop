from django.urls import path, re_path, register_converter

from catalog import converters, views

app_name = "catalog"

register_converter(converters.PositiveNumbersConverter, "pos")

urlpatterns = [
    path("", views.item_list, name="item_list"),
    path("<int:pk>/", views.item_detail, name="item_detail"),
    re_path(
        r"re/(?P<pk>[1-9][0-9]*)/",
        views.get_from_re_path,
        name="item_re",
    ),
    path(
        "converter/<pos:pk>/",
        views.get_from_converter,
        name="item_converter",
    ),
]
