from django.urls import path, re_path, register_converter

from catalog import converter, views

register_converter(converter.PositiveIntConverter, "pic")
app_name = "catalog"

urlpatterns = [
    path("", views.item_list, name="main"),
    path("<int:pk>/", views.item_detail, name="item_detail"),
    path("converter/<pic:number>/", views.extract_number, name="re"),
    re_path(
        r"^re/(?P<number>[1-9]\d*)/$",
        views.extract_number,
        name="converter",
    ),
]
