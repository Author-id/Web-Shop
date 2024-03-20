from django.conf import settings
from django.db import models
from django.utils.text import Truncator

__all__ = ["Status", "Feedback", "StatusLog"]


class Status(models.TextChoices):
    NEW = "Получено"
    PENDING = "В обработке"
    COMPLETE = "Ответ дан"


class Feedback(models.Model):
    name = models.CharField(
        "Имя",
        max_length=150,
        help_text="Ваше имя",
        null=True,
        blank=True,
    )
    text = models.TextField(
        verbose_name="Текст",
        help_text="Напишите текст письма",
        null=True,
    )
    created_on = models.DateTimeField(
        "Дата и время",
        auto_now_add=True,
        help_text="Время создания записи",
    )
    mail = models.EmailField(
        "Почта",
        help_text="Введите почту",
    )
    status = models.CharField(
        choices=Status.choices,
        default=Status.NEW,
        max_length=11,
        verbose_name="Статус",
        help_text="Статус письма",
    )

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"


class StatusLog(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
    )
    feedback = models.ForeignKey(
        Feedback,
        on_delete=models.SET_NULL,
        null=True,
    )
    timestamp = models.DateTimeField(
        verbose_name="Временная метка",
        help_text="Дата и время создания",
        auto_now_add=True,
        null=True,
    )
    _from = models.CharField(
        choices=Status.choices,
        db_column="from",
        max_length=11,
        verbose_name="От кого",
    )
    to = models.CharField(
        choices=Status.choices,
        max_length=11,
        verbose_name="Кому",
    )

    class Meta:
        verbose_name = "Журнал состояния"
        verbose_name_plural = "Журнал состояний"

    def __str__(self) -> str:
        return Truncator(f"Состояние ({self.id})").words(5)
