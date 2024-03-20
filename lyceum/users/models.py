from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db import models


__all__ = []


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
    coffee_count = models.IntegerField(
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
