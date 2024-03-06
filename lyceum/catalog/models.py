import django.core.validators
import django.db
from django.utils import timezone
from slugify import slugify
import tinymce.models

from catalog.validators import ValidateMustContain
from core.models import AbstractModel, BaseImage

__all__ = []


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
            self.slug = slugify(self.name)
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
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = "категория"
        verbose_name_plural = "категории"


class ItemManager(django.db.models.Manager):
    def published(self):
        return (
            self.get_queryset()
            .filter(is_published=True, category__is_published=True)
            .select_related("category", "main_image")
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
                "category__name",
                "text",
                "tags__name",
                "main_image__image",
            )
        )

    def on_main(self):
        return self.published().filter(is_on_main=True).order_by("name")

    def get_item(self):
        return (
            self.get_queryset()
            .filter(is_published=True, category__is_published=True)
            .select_related("category", "main_image")
            .prefetch_related(
                django.db.models.Prefetch(
                    "tags",
                    queryset=Tag.objects.filter(is_published=True).only(
                        "name",
                    ),
                ),
                django.db.models.Prefetch(
                    "images",
                    queryset=ItemSecondaryImage.objects.all(),
                ),
            )
            .only(
                "id",
                "name",
                "category__name",
                "text",
                "tags__name",
                "main_image__image",
                "images__image",
            )
        )


class Item(AbstractModel):
    objects = ItemManager()
    is_on_main = django.db.models.BooleanField(
        "в главном",
        default=False,
        help_text="находится на домашней странице",
    )
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
        related_query_name="items",
        help_text="выберите категорию",
    )
    tags = django.db.models.ManyToManyField(
        Tag,
        verbose_name="теги",
        related_name="items",
        related_query_name="items",
        help_text="выберите теги",
    )
    created = django.db.models.DateTimeField(
        verbose_name="создано",
        auto_now_add=True,
        null=True,
    )
    updated = django.db.models.DateTimeField(
        verbose_name="обновлено",
        editable=False,
        null=True,
    )

    def save(self, *args, **kwargs):
        if not self.updated:
            self.updated = self.created
        else:
            self.updated = timezone.now()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "товар"
        verbose_name_plural = "товары"


class ItemMainImage(BaseImage):
    item = django.db.models.OneToOneField(
        Item,
        on_delete=django.db.models.CASCADE,
        related_name="main_image",
        related_query_name="main_image",
    )

    class Meta:
        verbose_name = "главное изображение"
        verbose_name_plural = "главные изображения"


class ItemSecondaryImage(BaseImage):
    item = django.db.models.ForeignKey(
        Item,
        on_delete=django.db.models.CASCADE,
        related_name="images",
        related_query_name="images",
    )

    class Meta:
        verbose_name = "дополнительное изображение"
        verbose_name_plural = "дополнительные изображения"
