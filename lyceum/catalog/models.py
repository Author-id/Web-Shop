import django.core.validators
import django.db
import tinymce.models

from catalog.validators import ValidateMustContain
from core.models import AbstractModel, BaseImage, SlugFieldModel

__all__ = ["Category", "Item", "Tag"]


class ItemManager(django.db.models.Manager):
    def on_main(self):
        return (
            self.get_queryset()
            .filter(is_on_main=True)
            .filter(is_published=True)
            .select_related("category")
            .filter(category__is_published=True)
            .prefetch_related(
                django.db.models.Prefetch(
                    "tags",
                    queryset=Tag.objects.all()
                    .filter(is_published=True)
                    .only("name"),
                ),
            )
            .filter(tags__is_published=True)
            .only(
                "name",
                "text",
                "category_id",
                "category__name",
                "main_image__image",
                "images__image",
            )
        )

    def published(self):
        return (
            self.get_queryset()
            .filter(is_published=True)
            .filter(category__is_published=True)
            .select_related("category")
            .select_related("main_image")
            .prefetch_related(
                django.db.models.Prefetch(
                    "tags",
                    queryset=Tag.objects.filter(is_published=True).only(
                        "name",
                    ),
                ),
            )
            .only(
                "name",
                "text",
                "main_image__image",
                "category__name",
                "images__image",
            )
        )


class Tag(AbstractModel, SlugFieldModel):
    class Meta:
        db_table = "catalog_tag"
        verbose_name = "тег"
        verbose_name_plural = "теги"


class Category(AbstractModel, SlugFieldModel):
    weight = django.db.models.PositiveSmallIntegerField(
        "вес",
        default=100,
        validators=[
            django.core.validators.MaxValueValidator(32767),
            django.core.validators.MinValueValidator(1),
        ],
        help_text="ёмаё введите вес",
    )

    class Meta:
        ordering = ("name",)
        db_table = "catalog_category"
        verbose_name = "категория"
        verbose_name_plural = "категории"


class Item(AbstractModel):
    objects = ItemManager()

    is_on_main = django.db.models.BooleanField(default=False)
    text = tinymce.models.HTMLField(
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
        ordering = ("name",)
        db_table = "catalog_item"
        verbose_name = "товар"
        verbose_name_plural = "товары"


class Images(BaseImage):
    item = django.db.models.ForeignKey(
        Item,
        on_delete=django.db.models.CASCADE,
        related_name="images",
        related_query_name="images",
    )

    class Meta:
        db_table = "catalog_images"
        verbose_name = "дополнительное изображение"
        verbose_name_plural = "дополнительные изображения"


class MainImage(BaseImage):
    item = django.db.models.OneToOneField(
        Item,
        on_delete=django.db.models.CASCADE,
        related_name="main_image",
    )

    class Meta:
        db_table = "catalog_image"
        verbose_name = "главное изображение"
        verbose_name_plural = "главные изображения"
