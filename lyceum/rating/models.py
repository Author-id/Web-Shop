from django.db import models
from django.contrib.auth.models import User
from catalog.models import Item


class Rating(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    item = models.ForeignKey(
        Item,
        on_delete=models.CASCADE,
    )
    rating = models.IntegerField(
        choices=[
            (1, "Ненависть"),
            (2, "Неприязнь"),
            (3, "Нейтрально"),
            (4, "Обожание"),
            (5, "Любовь"),
        ]
    )

    class Meta:
        unique_together = ("user", "item")
