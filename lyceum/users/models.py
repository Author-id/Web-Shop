from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(
        "Биография",
        blank=True,
        null=True,
    )
    birthday = models.DateField(
        "Дата рождения",
        blank=True,
        null=True,
        help_text="Введите дату рождения пользователя",
    )
    coffe_count = models.IntegerField(
        "Сколько раз пользователь пил кофе",
        default=0,
        blank=False,
        null=False,
        help_text="Количество переходов по /coffee/",
    )
    image = models.ImageField(
        "Аватар",
        default=None,
        blank=True,
        null=True,
        help_text="Аватар пользователя",
    )

    class Meta:
        verbose_name = "Дополнительное поле"
        verbose_name_plural = "Дополнительные поля"

