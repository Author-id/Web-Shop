from typing import Any

from django.contrib.auth import views
from django.contrib.auth.forms import AuthenticationForm
from django.urls import path

import users.views


class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control"


app_name = "users"

urlpatterns = [
    path(
        "login/",
        views.LoginView.as_view(
            template_name="users/login.html",
            authentication_form=CustomAuthenticationForm,
        ),
        name="user",
    ),
    path(
        "logout/",
        views.LogoutView.as_view(),
        name="exit",
    ),
    path(
        "reg/",
        users.views.register,
        name="reg",
    )
]


__all__: list[str] = []

