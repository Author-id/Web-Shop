from django.urls import path, re_path, register_converter

from . import converters
from .views import (
    item_detail,
    item_detail_converter,
    item_detail_re,
    item_list,
)

register_converter(converters.PositiveIdConverter, "positiveid")

urlpatterns = [
    path("catalog/", item_list),
    path("catalog/<int:pk>/", item_detail),
    re_path(r"^catalog/re/(?P<pk>[1-9]\d*/)", item_detail_re),
    path("catalog/converter/<positiveid:pk>/", item_detail_converter),
]
