import sys
from typing import cast, Optional

from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db import models


__all__ = []

if "makemigrations" not in sys.argv and "migrate" not in sys.argv:
    User._meta.get_field("email")._unique = True


class Profile(models.Model):
    def upload_to(self, filename):
        return f"uploads/{self.image}/{filename}"

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
    coffee_count = models.PositiveIntegerField(
        "Сколько раз пользователь пил кофе",
        default=0,
        validators=[MinValueValidator(0)],
        help_text="Количество переходов по /coffee/",
    )
    image = models.ImageField(
        "Аватар",
        default=None,
        blank=True,
        null=True,
        help_text="Аватар пользователя",
        upload_to=upload_to,
    )

    class Meta:
        verbose_name = "Дополнительное поле"
        verbose_name_plural = "Дополнительные поля"


class UserManager(models.Manager):
    def get_queryset(self) -> models.query.QuerySet:
        return (
            super()
            .get_queryset()
            .select_related(
                User.profile.related.name,
            )
        )

    def active(self) -> models.query.QuerySet:
        return self.get_queryset().filter(is_active=True)

    def by_mail(self, mail: str) -> "User | None":
        return cast(Optional[User], self.get_queryset().get(email=mail))


class User(get_user_model()):
    objects = UserManager()

    class Meta:
        proxy = True
