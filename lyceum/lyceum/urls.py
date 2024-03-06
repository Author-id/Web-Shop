from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from lyceum import settings


urlpatterns = [
    path(
        "",
        include(("homepage.urls")),
        name="homepage",
    ),
    path(
        "about/",
        include(("about.urls")),
        name="about",
    ),
    path(
        "catalog/",
        include(("catalog.urls")),
        name="catalog",
    ),
    path(
        "admin/",
        admin.site.urls,
        name="admin",
    ),
    path(
        "tinymce/",
        include("tinymce.urls"),
    ),
]

if settings.DEBUG:
    urlpatterns += (path("__debug__/", include("debug_toolbar.urls")),)
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )
