from django.contrib.auth.models import User
from django.db import models

from catalog.models import Item


class RatingChoices(models.IntegerChoices):
    HATE = 1, "Ненависть"
    DISLIKE = 2, "Неприязнь"
    NEUTRAL = 3, "Нейтрально"
    ADORE = 4, "Обожание"
    LOVE = 5, "Любовь"


class Rating(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    item = models.ForeignKey(
        Item,
        on_delete=models.CASCADE,
    )
    rating = models.IntegerField(choices=RatingChoices.choices)

    class Meta:
        unique_together = ("user", "item")


__all__ = []
