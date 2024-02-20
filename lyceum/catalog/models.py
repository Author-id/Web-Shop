from core.models import AbstractModel
import django.core.validators

from django.db import models


def good_word_validator(value):
    print(value)
    if not ("превосходно" in value.lower() or "роскошно" in value.lower()):
        raise django.core.exceptions.ValidationError(
            "В тексте должно быть слово `превосходно` или `роскошно`"
        )


def slug_validator(value):
    chars = "0123456789-_abcdefghijklmnopqrstuvwxyz"
    for c in value:
        if c.lower() not in chars:
            raise django.core.exceptions.ValidationError(
                "Допускаюстя только цифры, буквы латиницы и символы - и _"
            )


class Tag(AbstractModel):
    slug = models.CharField(
        verbose_name="Слаг",
        max_length=200,
        unique=True,
        validators=[slug_validator],
        help_text="help_text",
    )

    class Meta:
        db_table = "catalog_tag"
        verbose_name = "тег"
        verbose_name_plural = "теги"


class Category(AbstractModel):
    slug = models.CharField(
        verbose_name="Слаг",
        max_length=200,
        unique=True,
        validators=[slug_validator],
        help_text="help_text",
    )

    weight = models.IntegerField(
        verbose_name="Вес",
        default=100,
        validators=[
            django.core.validators.MinValueValidator(0),
            django.core.validators.MaxValueValidator(32767),
        ],
        help_text="help_text",
    )

    class Meta:
        db_table = "catalog_category"
        verbose_name = "категория"
        verbose_name_plural = "категории"


class Item(AbstractModel):
    text = models.TextField(
        verbose_name="Текст",
        validators=[good_word_validator],
        help_text="help_text",
    )

    category = models.ForeignKey(
        "category",
        verbose_name="Категория",
        on_delete=models.CASCADE,
        default=None,
        blank=True,
        null=True,
        help_text="help_text",
    )

    tags = models.ManyToManyField(Tag)

    class Meta:
        db_table = "catalog_item "
        verbose_name = "товар"
        verbose_name_plural = "товары"
