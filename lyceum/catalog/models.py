from django.core.exceptions import ValidationError
from core.models import AbstractModel
import django.core.validators

import django.db


def perfect_in_text_validator(value):
    value = value.lower().split()
    if "превосходно" not in value and "роскошно" not in value:
        raise ValidationError("нет слова превосходно или роскошно в тексте")


class Tag(AbstractModel):
    slug = django.db.models.CharField(
        "Слаг",
        max_length=200,
        unique=True,
        validators=[
            django.core.validators.RegexValidator("^[a-zA-Z0-9+_-]*$")
        ],
        help_text="я сам не понял что это",
    )

    class Meta:
        db_table = "catalog_tag"
        verbose_name = "тег"
        verbose_name_plural = "теги"


class Category(AbstractModel):
    slug = django.db.models.CharField(
        "Слаг",
        max_length=200,
        unique=True,
        validators=[
            django.core.validators.RegexValidator("^[a-zA-Z0-9+_-]*$")
        ],
        help_text="сам не знаю что это",
    )
    weight = django.db.models.IntegerField(
        "Вес",
        default=100,
        validators=[
            django.core.validators.MaxValueValidator(32767),
            django.core.validators.MinValueValidator(0),
        ],
        help_text="ну какой вес то",
    )

    class Meta:
        db_table = "catalog_category"
        verbose_name = "категория"
        verbose_name_plural = "категории"


class Item(AbstractModel):
    text = django.db.models.TextField(
        "Текст",
        validators=[
            perfect_in_text_validator,
        ],
        help_text="опишите",
    )
    category = django.db.models.ForeignKey(
        Category,
        on_delete=django.db.models.CASCADE,
        related_name="items",
        help_text="выберите категорию",
    )
    tags = django.db.models.ManyToManyField(
        Tag,
        related_name="tags",
        help_text="выберите теги",
    )

    class Meta:
        db_table = "catalog_item"
        verbose_name = "товар"
        verbose_name_plural = "товары"
