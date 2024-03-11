from django.conf import settings
import django.db


__all__ = []


class Status(django.db.models.TextChoices):
    NEW = "получено"
    PENDING = "в обработке"
    COMPLETE = "ответ дан"


class Feedback(django.db.models.Model):
    name = django.db.models.CharField(
        "имя",
        max_length=150,
        help_text="напишите имя",
        null=True,
        blank=True,
    )
    text = django.db.models.TextField(
        "текст",
        help_text="напишите текст сообщения",
    )
    created_on = django.db.models.DateTimeField(
        verbose_name="создано",
        help_text="дата и время создания",
        auto_now_add=True,
        null=True,
    )
    mail = django.db.models.EmailField(
        verbose_name="почта",
        help_text="почтовый адрес",
    )
    status = django.db.models.CharField(
        choices=Status.choices,
        default=Status.NEW,
        max_length=11,
        verbose_name="статус",
    )

    class Meta:
        verbose_name = "обратная связь"
        verbose_name_plural = "обратные связи"

    def __str__(self) -> str:
        return f"обратная связь ({self.id})"


class StatusLog(django.db.models.Model):
    user = django.db.models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=django.db.models.SET_NULL,
        null=True,
    )
    feedback = django.db.models.ForeignKey(
        Feedback,
        on_delete=django.db.models.SET_NULL,
        null=True,
    )
    timestamp = django.db.models.DateTimeField(
        verbose_name="создано",
        help_text="дата и время создания",
        auto_now_add=True,
        null=True,
    )
    _from = django.db.models.CharField(
        choices=Status.choices,
        db_column="from",
        max_length=11,
        verbose_name="от",
    )
    to = django.db.models.CharField(
        choices=Status.choices,
        max_length=11,
        verbose_name="от",
    )

    class Meta:
        verbose_name = "журнал состояния"
        verbose_name_plural = "журнал состояний"

    def __str__(self) -> str:
        return f"состояние ({self.id})"

