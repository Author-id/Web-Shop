import string
import django.core.exceptions

import core.models
import django.core.validators
import django.db


def perfect_validator(value):
    if "превосходно" not in value.lower():
        if "роскошно" not in value.lower():
            raise django.core.exceptions.ValidationError(
                "Обязательно должно содержаться слово `превосходно`"
                "или `роскошно`"
            )


def slug_validator(value):
    allowed = string.ascii_lowercase + string.digits + "_-"
    for i in value:
        if i not in allowed:
            raise django.core.exceptions.ValidationError(
                "В поле должны содержаться только "
                "буквы, цифры и некоторые символы"
            )


class Tag(core.models.AbstractModel, django.db.models.Model):
    slug = django.db.models.CharField(
        verbose_name="слаг",
        max_length=200,
        unique=True,
        validators=[
            django.core.validators.MaxLengthValidator(200),
            slug_validator,
        ],
    )

    class Meta:
        db_table = "catalog_tag"
        verbose_name = "тег"
        verbose_name_plural = "теги"

    def __str__(self):
        return self.name[:15]


class Category(core.models.AbstractModel, django.db.models.Model):
    slug = django.db.models.CharField(
        verbose_name="слаг",
        max_length=200,
        unique=True,
        validators=[
            slug_validator,
            django.core.validators.MaxLengthValidator(200),
        ],
    )

    weight = django.db.models.IntegerField(
        verbose_name="Вес",
        default=100,
        validators=[
            django.core.validators.MinValueValidator(0),
            django.core.validators.MaxValueValidator(32767),
        ],
    )

    class Meta:
        db_table = "catalog_category"
        verbose_name = "категория"
        verbose_name_plural = "категории"

    def __str__(self):
        return self.name[:15]


class Item(core.models.AbstractModel, django.db.models.Model):
    category = django.db.models.ForeignKey(
        Category,
        on_delete=django.db.models.CASCADE,
        verbose_name="категория",
    )

    tags = django.db.models.ManyToManyField(Tag)

    text = django.db.models.TextField(
        verbose_name="описание", validators=[perfect_validator]
    )

    class Meta:
        db_table = "catalog_item"
        verbose_name = "товар"
        verbose_name_plural = "товары"

    def __str__(self):
        return self.name[:15]
