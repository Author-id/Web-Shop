from django.contrib.auth.forms import UserCreationForm
import django.forms

import users.models


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


class BootstrapModelForm(django.forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control"


class ProfileForm(BootstrapModelForm):
    class Meta(UserCreationForm.Meta):
        model = users.models.Profile
        fields = [
            model.birthday.field.name,
            model.image.field.name,
            model.coffee_count.field.name,
        ]

        widgets = {
            model.coffee_count.field.name: django.forms.NumberInput(
                attrs={
                    "readonly": "readonly",
                    "disabled": "disabled",
                },
            ),
        }


class CustomUserChangeForm(
    django.contrib.auth.forms.UserChangeForm,
    BootstrapModelForm,
):
    class Meta(django.contrib.auth.forms.UserChangeForm.Meta):
        fields = (
            "email",
            "username",
            "first_name",
            "last_name",
        )


class SignUpForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        fields = ("username", "email")
