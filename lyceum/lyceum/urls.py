from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, reverse_lazy
from django.contrib.auth import views
from django.contrib.auth.forms import (
    AuthenticationForm,
    PasswordChangeForm,
    PasswordResetForm,
    SetPasswordForm,
)
from users.urls import custom_auth_form
import users.views


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
        "feedback/",
        include(("feedback.urls")),
        name="feedback",
    ),
    path(
        "admin/",
        admin.site.urls,
        name="admin",
    ),
    path(
        "download/",
        include(("download.urls")),
        name="download",
    ),
    path(
        "tinymce/",
        include(("tinymce.urls")),
    ),
    path(
        "i18n/",
        include(("django.conf.urls.i18n")),
    ),
    path(
        "login/",
        views.LoginView.as_view(
            template_name="users/login.html",
            authentication_form=custom_auth_form(AuthenticationForm),
        ),
        name="login",
    ),
    path(
        "logout/",
        views.LogoutView.as_view(),
        name="logout",
    ),
    path(
        "reg/",
        users.views.register,
        name="reg",
    ),
path(
        "password_change/",
        views.PasswordChangeView.as_view(
            template_name="users/password_change.html",
            form_class=custom_auth_form(PasswordChangeForm),
        ),
        name="password_change",
    ),
    path(
        "password_change/done/",
        views.PasswordChangeDoneView.as_view(
            template_name="users/password_change_done.html",
        ),
        name="password_change_done",
    ),
    path(
        "password_reset/",
        views.PasswordResetView.as_view(
            template_name="users/password_reset.html",
            email_template_name="users/password_reset_email.html",
            form_class=custom_auth_form(PasswordResetForm),
            success_url=reverse_lazy("users:password_reset_done"),
        ),
        name="password_reset",
    ),
    path(
        "password_reset/done/",
        views.PasswordResetDoneView.as_view(
            template_name="users/password_reset_done.html",
        ),
        name="password_reset_done",
    ),
    path(
        "password_reset_confirm/<uidb64>/<token>/",
        views.PasswordResetConfirmView.as_view(
            form_class=custom_auth_form(SetPasswordForm),
            template_name="users/password_reset_confirm.html",
            success_url=reverse_lazy("users:password_reset_confirm_complite"),
        ),
        name="password_reset_confirm",
    ),
    path(
        "password_reset_complite",
        views.PasswordResetCompleteView.as_view(
            template_name="users/password_reset_complite.html",
        ),
        name="password_reset_complite",
    ),
]

if settings.DEBUG:
    urlpatterns += (path("__debug__/", include("debug_toolbar.urls")),)
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )
