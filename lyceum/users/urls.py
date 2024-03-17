from django.contrib.auth import views
from django.contrib.auth.forms import (
    AuthenticationForm,
    PasswordChangeForm,
    PasswordResetForm,
    SetPasswordForm,
)
import django.forms
from django.urls import path, reverse_lazy

__all__ = []


def custom_auth_form(form):
    class CustomForm(form):
        def __init__(self, *args, **kwargs) -> None:
            super().__init__(*args, **kwargs)
            for field in self.visible_fields():
                if isinstance(field.field.widget, django.forms.CheckboxInput):
                    field.field.widget.attrs["class"] = "form-check-input"
                else:
                    field.field.widget.attrs["class"] = "form-control"

    return CustomForm


app_name = "users"

urlpatterns = [
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


