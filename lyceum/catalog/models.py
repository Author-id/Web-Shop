import django.core.exceptions
import django.core.validators
import django.db.models

import catalog.validators
from core.models import AbstractModel, BaseModel


class Tag(AbstractModel, BaseModel):
    slug = django.db.models.SlugField(
        max_length=200,
        unique=True,
        verbose_name="слаг",
    )

    class Meta:
        db_table = "catalog_tag"
        verbose_name = "тег"
        verbose_name_plural = "теги"

    def __str__(self):
        return self.name[:15]


class Category(AbstractModel, BaseModel):
    slug = django.db.models.SlugField(
        max_length=200,
        unique=True,
        verbose_name="слаг",
    )
    weight = django.db.models.IntegerField(
        default=100,
        validators=[
            django.core.validators.MaxValueValidator(32767),
            django.core.validators.MinValueValidator(1),
        ],
        verbose_name="вес",
    )

    class Meta:
        db_table = "catalog_category"
        verbose_name = "категория"
        verbose_name_plural = "категории"

    def __str__(self):
        return self.name[:15]


class Item(AbstractModel):
    text = django.db.models.TextField(
        validators=[
            catalog.validators.ValidateMustContain("превосходно", "роскошно"),
            django.core.validators.MinLengthValidator(2),
        ],
        verbose_name="текст",
        help_text="Описание должно быть больше, чем из 2х слов "
        "и содержать слова 'превосходно, роскошно'",
    )
    category = django.db.models.ForeignKey(
        Category,
        on_delete=django.db.models.CASCADE,
        related_name="items",
        null=True,
        verbose_name="категория",
        help_text="Выберите категорию",
    )
    tags = django.db.models.ManyToManyField(
        Tag,
        related_name="tags",
        verbose_name="тег",
        help_text="Удерживайте 'Control' (или 'Command' "
        "на Mac), чтобы выбрать несколько значений",
    )

    class Meta:
        db_table = "catalog_item"
        verbose_name = "товар"
        verbose_name_plural = "товары"

    def __str__(self):
        return self.text[:15]
