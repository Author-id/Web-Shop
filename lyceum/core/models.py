import re

import django.core.exceptions
import django.db.models
import django.core.validators


def normalize_name(name):
    name = "".join(name.split())
    lower_string = name.lower()
    no_number_string = re.sub(r"\d+", "", lower_string)
    no_punc_string = re.sub(r"[^\w\s]", "", no_number_string)
    no_wspace_string = no_punc_string.strip()
    pattern = r"(.)\1+"
    repl = r"\1"
    name = re.sub(pattern, repl, no_wspace_string)
    similar_chars = {
        "а": "a",
        "о": "o",
        "у": "y",
        "е": "e",
        "с": "c",
        "м": "m",
        "р": "p",
        "т": "t",
        "х": "x",
        "в": "b",
        "к": "k",
        "н": "h",
        "г": "r",
    }
    for word, replacement in similar_chars.items():
        name = name.replace(word, replacement)
    return name


class BaseModel(django.db.models.Model):
    normalized_name = django.db.models.CharField(
        unique=True,
        editable=False,
        max_length=150,
        validators=[
            django.core.validators.MaxLengthValidator(150),
        ],
        null=True,
    )

    def clean(self) -> None:
        normalized = normalize_name(self.name)
        existing = self.__class__.objects.filter(
            normalized_name=normalized,
        )
        if existing:
            raise django.core.exceptions.ValidationError(
                {
                    self.__class__.name.field.name: "Такое имя уже имеется",
                },
            )
        self.normalized_name = normalized

    class Meta:
        abstract = True


class AbstractModel(django.db.models.Model):
    is_published = django.db.models.BooleanField(
        default=True,
        verbose_name="опубликовано",
    )
    name = django.db.models.CharField(
        max_length=150,
        verbose_name="название",
        help_text="max 150 символов",
        unique=True,
    )

    class Meta:
        abstract = True
