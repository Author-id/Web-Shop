from django.test import Client, override_settings, TestCase
from django.urls import reverse
import settings

__all__ = ["ReverseResponseMiddlewareTests"]


class ReverseResponseMiddlewareTests(TestCase):
    @override_settings(ALLOW_REVERSE=True)
    def test_reverse_russian_words_enabled(self):
        contents = [
            Client().get(reverse("homepage:coffee")).content.decode()
            for _ in range(20)
        ]
        self.assertIn(
            "Я кинйач",
            contents,
            "'Я кинйач' not in twenty requests",
        )
        self.assertEqual(
            contents.count("Я кинйач"),
            2,
            "count 'Я кинйач' in twenty requests != 2",
        )
        content_first, content_second = list(
            filter(lambda content: content == "Я кинйач", contents),
        )
        first = contents.index(content_first)
        second = 20 - contents[-1::-1].index(content_second) - 1
        self.assertEqual(
            second - first,
            10,
            "difference between index 'Я кинйач' != 10",
        )

    @override_settings(ALLOW_REVERSE=False)
    def test_reverse_russian_words_disabled(self):
        contents = [
            Client().get(reverse("homepage:coffee")).content.decode()
            for _ in range(20)
        ]
        self.assertNotIn("Я кинйач", contents, "'Я кинйач' in twenty contents")

    def test_reverse_russian_words_enabled_default(self) -> None:
        contents = [
            Client().get(reverse("homepage:coffee")).content.decode()
            for _ in range(20)
        ]
        if settings.ALLOW_REVERSE:
            self.assertIn(
                "Я кинйач",
                contents,
                "'Я кинйач' not in twenty requests",
            )
            self.assertEqual(
                contents.count("Я кинйач"),
                2,
                "count 'Я кинйач' in twenty requests != 2",
            )
            content_first, content_second = list(
                filter(lambda content: content == "Я кинйач", contents),
            )
            first = contents.index(content_first)
            second = 20 - contents[-1::-1].index(content_second) - 1
            self.assertEqual(
                second - first,
                10,
                "difference between index 'Я кинйач' != 10",
            )
        else:
            self.assertNotIn(
                "Я кинйач",
                contents,
                "'Я кинйач' in twenty requests",
            )
