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

    def clean_email(self):
        email = self.cleaned_data.get("email")
        email = users.models.UserManager().normalize_email(email)
        try:
            users.models.User.objects.by_mail(mail=email)
            raise django.forms.ValidationError(
                "Пользователь с такой почтой уже существует.",
            )
        except users.models.User.DoesNotExist:
            return email


class CustomAuthenticationForm(
    django.contrib.auth.forms.AuthenticationForm,
    BootstrapModelForm,
):
    username = django.forms.CharField(
        label="Почта или имя пользователя",
        max_length=254,
    )

    class Meta:
        model = django.contrib.auth.get_user_model()
        fields = (model.username.field.name, model.password.field.name)

    def clean(self):
        username_or_email = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")

        if username_or_email and password:
            user = django.contrib.auth.authenticate(
                username=username_or_email,
                password=password,
            )
            if not user:
                email = users.models.UserManager().normalize_email(
                    username_or_email,
                )
                user = django.contrib.auth.authenticate(
                    email=email,
                    password=password,
                )

            if not user:
                raise django.forms.ValidationError(
                    "Неправильные логин или пароль.",
                )

        return super(CustomAuthenticationForm, self).clean()
