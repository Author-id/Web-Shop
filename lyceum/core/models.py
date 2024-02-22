import django.db


class AbstractModel(django.db.models.Model):
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

    class Meta:
        abstract = True

    def __str__(self):
        return self.name
