import django.core.validators
import django.db.models


class AbstractModel(django.db.models.Model):

    is_published = django.db.models.BooleanField(
        verbose_name="Опубликовано",
        default=True,
    )

    name = django.db.models.CharField(
        verbose_name="Название",
        max_length=150,
        validators=[django.core.validators.MaxLengthValidator(150)],
    )

    class Meta:
        abstract = True

    def __str__(self):
        return self.name[:15]
