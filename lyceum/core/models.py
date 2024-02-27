from pathlib import Path
import re

from django.core.exceptions import ValidationError
import django.db
from django.utils.safestring import mark_safe
from slugify import slugify
import sorl

__all__ = ["AbstractModel", "normalize_str"]


def normalize_str(value):
    words = re.findall("[0-9а-яёa-z]+", value.lower())
    return slugify("".join(words))


class AbstractModel(django.db.models.Model):
    objects = django.db.models.Manager()
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
    normalize_name = django.db.models.CharField(
        "нормализованное название",
        max_length=150,
        unique=True,
        editable=False,
        help_text="этот field не редактируется и нормализует field(name)",
    )

    class Meta:
        verbose_name = "абстрактная модель"
        verbose_name_plural = "абстрактная модели"
        abstract = True

    def clean(self):
        normalize_name = normalize_str(self.name)
        found = self.__class__.objects.filter(
            normalize_name=normalize_name,
        )
        if found and found[0] != self:
            raise ValidationError(
                {self.__class__.name.field.name: "есть похожое название"},
            )
        self.normalize_name = normalize_name

    def __str__(self) -> str:
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
