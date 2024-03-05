from django.contrib import admin
from django.urls import include, path

from lyceum import settings

urlpatterns = [
    path("admin/", admin.site.urls, name="admin"),
    path("", include("homepage.urls"), name="homepage"),
    path("catalog/", include("catalog.urls"), name="catalog"),
    path("about/", include("about.urls"), name="about"),
]
if settings.DEBUG:
    import debug_toolbar

    urlpatterns += (path("__debug__/", include(debug_toolbar.urls)),)
