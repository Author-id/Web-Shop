from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class UserRegisterForm(UserCreationForm):
    username = forms.CharField(
        label="Введите логин",
        required=True,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Введите логин"}),
    )
    #some = forms.ModelChoiceField(queryset=User.objects.all())
    password1 = forms.CharField(
        label="Введите пароль",
        required=True,
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Введите пароль"})
    )
    password2 = forms.CharField(
        label="Подтвердите пароль",
        required=True,
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Повторите пароль"})

    )

    class Meta:
        model = User
        fields = ["username", "password1", "password2"]

