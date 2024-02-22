import django.core.validators
import django.db

from catalog.validators import ValidateMustContain
from core.models import AbstractModel


class Tag(AbstractModel):
    slug = django.db.models.SlugField(
        "слаг",
        max_length=200,
        unique=True,
        help_text="Какая-то дичь",
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
        help_text="Какая-то дичь",
    )
    weight = django.db.models.IntegerField(
        "вес",
        default=100,
        validators=[
            django.core.validators.MaxValueValidator(32767),
            django.core.validators.MinValueValidator(1),
        ],
        help_text="ёмаё введите вес",
    )

    class Meta:
        db_table = "catalog_category"
        verbose_name = "категория"
        verbose_name_plural = "категории"


class Item(AbstractModel):
    text = django.db.models.TextField(
        "текст",
        validators=[
            ValidateMustContain("превосходно", "роскошно"),
        ],
        help_text="Описание",
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
