from django.urls import path, re_path, register_converter

from catalog import converters
from catalog.views import (
    item_detail,
    item_detail_converter,
    item_detail_re,
    item_list,
)

register_converter(converters.PositiveIdConverter, "positive")

urlpatterns = [
    path("", item_list),
    path("<int:pk>/", item_detail),
    re_path(r"^re/(?P<pk>[1-9]\d*/)", item_detail_re),
    path("converter/<positive:pk>/", item_detail_converter),
]
