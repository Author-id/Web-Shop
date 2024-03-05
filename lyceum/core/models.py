from pathlib import Path

import django.db
from django.utils.safestring import mark_safe
import sorl

__all__ = ["AbstractModel", "BaseImage", "SlugFieldModel"]


class AbstractModel(django.db.models.Model):
    name = django.db.models.CharField(
        "название",
        max_length=150,
        unique=True,
        help_text="Напишите название",
    )
    is_published = django.db.models.BooleanField(
        "опубликовано",
        default=True,
        help_text="поставьте галочку если он опубликован",
    )

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class SlugFieldModel(django.db.models.Model):
    slug = django.db.models.SlugField(
        "слаг",
        max_length=200,
        unique=True,
        help_text="Какая-то дичь",
    )

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class BaseImage(django.db.models.Model):
    image = sorl.thumbnail.ImageField(
        upload_to="catalog/items/",
        verbose_name="изображение",
    )

    def get_image_300x300(self):
        return sorl.thumbnail.get_thumbnail(
            self.image,
            "300x300",
            crop="center",
            quality=51,
        )

    def image_tmb(self):
        if self.image:
            tag = f'<img src="{self.get_image_300x300().url}">'
            return mark_safe(tag)
        return "изображение отсутствует"

    image_tmb.short_description = "превью"
    image_tmb.allow_tags = True
    image_tmb.field_name = "image_tmb"

    class Meta:
        abstract = True

    def __str__(self):
        return Path(self.image.path).stem
