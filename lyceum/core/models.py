from django.db import models


class AbstractModel(models.Model):
    is_published = models.BooleanField(
        verbose_name="Опубликовано", default=True
    )
    name = models.CharField(
        verbose_name="Название", max_length=150, default=""
    )

    class Meta:
        abstract = True

    def __str__(self):
        return self.name[:15]
