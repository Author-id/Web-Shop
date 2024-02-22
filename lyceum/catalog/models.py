import re

from django.core.exceptions import ValidationError
import django.core.validators
import django.db


from core.models import AbstractModel


def perfect_in_text_validator(value):
    if re.findall(r"\bпревосходно\b|\bроскошно\b", value, re.IGNORECASE):
        return
    raise ValidationError(
        "Должно содержаться слово 'превосходно' или 'роскошно'.",
    )


class Tag(AbstractModel):
    slug = django.db.models.SlugField(
        "слаг",
        max_length=200,
        unique=True,
        help_text="я сам не понял что это",
    )

    class Meta:
        db_table = "catalog_tag"
        verbose_name = "тег"
        verbose_name_plural = "теги"


class Category(AbstractModel):
    slug = django.db.models.SlugField(
        "слаг",
        max_length=200,
        unique=True,
        help_text="я сам не понял что это",
    )
    weight = django.db.models.IntegerField(
        "вес",
        default=100,
        validators=[
            django.core.validators.MaxValueValidator(32767),
            django.core.validators.MinValueValidator(1),
        ],
        help_text="ну какой вес то",
    )

    class Meta:
        db_table = "catalog_category"
        verbose_name = "категория"
        verbose_name_plural = "категории"


class Item(AbstractModel):
    text = django.db.models.TextField(
        "текст",
        validators=[
            perfect_in_text_validator,
        ],
        help_text="опишите",
    )
    category = django.db.models.ForeignKey(
        Category,
        on_delete=django.db.models.CASCADE,
        verbose_name="категория",
        related_name="items",
        help_text="выберите категорию",
    )
    tags = django.db.models.ManyToManyField(
        Tag,
        verbose_name="теги",
        related_name="items",
        help_text="выберите теги",
    )

    class Meta:
        db_table = "catalog_item"
        verbose_name = "товар"
        verbose_name_plural = "товары"
