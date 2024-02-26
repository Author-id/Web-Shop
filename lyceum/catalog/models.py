import django.core.validators
import django.db
import slugify
import tinymce.models

from catalog.validators import ValidateMustContain
from core.models import AbstractModel, BaseImage

__all__ = ["Category", "Item", "Tag"]


class Tag(AbstractModel):
    slug = django.db.models.SlugField(
        "слаг",
        max_length=200,
        unique=True,
        blank=True,
        help_text="строка идентификатор"
        "(заполните чтобы изменить автоматический слаг)",
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify.slugify(self.name)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "тег"
        verbose_name_plural = "теги"


class Category(AbstractModel):
    slug = django.db.models.SlugField(
        "слаг",
        max_length=200,
        unique=True,
        blank=True,
        help_text="строка идентификатор"
        "(заполните чтобы изменить автоматический слаг)",
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

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify.slugify(self.name)
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = "категория"
        verbose_name_plural = "категории"


class Item(AbstractModel):
    text = tinymce.models.HTMLField(
        "текст",
        validators=[
            ValidateMustContain("превосходно", "роскошно"),
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
        verbose_name = "товар"
        verbose_name_plural = "товары"


class ItemMainImage(BaseImage):
    item = django.db.models.OneToOneField(
        Item,
        on_delete=django.db.models.CASCADE,
        related_name="main_image",
    )

    class Meta:
        verbose_name = "главное изображение"
        verbose_name_plural = "главные изображения"


class ItemSecondaryImage(BaseImage):
    item = django.db.models.ForeignKey(
        Item,
        on_delete=django.db.models.CASCADE,
        related_name="images",
    )

    class Meta:
        verbose_name = "дополнительное изображение"
        verbose_name_plural = "дополнительные изображения"
