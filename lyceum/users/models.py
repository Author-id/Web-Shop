import sys

from django.contrib.auth import get_user_model
from django.contrib.auth.models import BaseUserManager, User
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import Q

__all__ = []

if "makemigrations" not in sys.argv and "migrate" not in sys.argv:
    User._meta.get_field("email")._unique = True


class Profile(models.Model):
    def image_path(self, filename):
        return f"users/{self.user.id}/{filename}"

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
    attempts_count = models.PositiveIntegerField(
        "попытки аутентификации",
        default=0,
    )

    block_date = models.DateTimeField(
        "дата блокировки аккаунта",
        null=True,
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
        upload_to=image_path,
    )

    class Meta:
        verbose_name = "дополнительное поле"
        verbose_name_plural = "дополнительные поля"


class UserManager(BaseUserManager):
    def normalize_email(self, email):
        email = super().normalize_email(email)
        try:
            email_name, domain_part = email.strip().rsplit("@", 1)
            email_name, domain_part = email_name.lower(), domain_part.lower()
        except ValueError:
            pass
        else:
            if "+" in email_name:
                email_name = email_name.split("+")[0]

            if domain_part == "yandex.ru" or domain_part == "ya.ru":
                domain_part = "yandex.ru"
                email_name = email_name.replace(".", "-")

            elif domain_part == "gmail.com":

                email_name = email_name.replace(".", "")

            email = email_name + "@" + domain_part

        return email

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

    def by_mail(self, mail):
        mail = self.normalize_email(mail)
        return self.get_queryset().get(email=mail)

    def get_by_natural_key(self, username):
        return (
            self.get_queryset()
            .filter(
                Q(email=self.normalize_email(username)) | Q(username=username),
            )
            .first()
        )


class User(get_user_model()):
    objects = UserManager()

    class Meta:
        proxy = True
