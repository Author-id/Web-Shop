import re

from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible


@deconstructible
class ValidateMustContain:
    def __init__(self, *args):
        self.contain = list(args)
        self.pattern = "|".join([f"\\b{word}\\b" for word in args])

    def __call__(self, val):
        if re.findall(r"\bпревосходно\b|\bроскошно\b", val, re.IGNORECASE):
            return
        raise ValidationError(
            "Должно содержаться слово 'превосходно' или 'роскошно'.",
        )
