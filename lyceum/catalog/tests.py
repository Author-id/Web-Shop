from http import HTTPStatus

from django.core.exceptions import ValidationError
from django.test import Client, TestCase
from django.urls import reverse
import parameterized

import catalog.models

__all__ = [
    "StaticURLTest",
    "RegexEndpointTest",
    "ConverterEndpointTest",
    "DBItemTests",
    "DBTagTests",
    "CategoryTests",
    "ContextTests",
]


class ContextTests(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.published_category = catalog.models.Category.objects.create(
            is_published=True,
            name="Test category",
            slug="publ_category",
            weight=100,
        )
        cls.unpublished_category = catalog.models.Category.objects.create(
            is_published=False,
            name="Test category unp",
            slug="unpubl_category",
            weight=100,
        )
        cls.published_tag = catalog.models.Tag.objects.create(
            is_published=True,
            name="Test publ tag",
            slug="publ_tag",
        )
        cls.unpublished_tag = catalog.models.Tag.objects.create(
            is_published=False,
            name="Test unpubl tag",
            slug="unpubl_tag",
        )
        cls.published_item = catalog.models.Item.objects.create(
            is_published=True,
            name="Test publ item",
            category=cls.published_category,
            text="роскошно",
        )
        cls.unpublished_item = catalog.models.Item.objects.create(
            is_published=False,
            name="Test unpubl item",
            category=cls.unpublished_category,
            text="превосходно",
        )

        cls.published_category.save()
        cls.unpublished_category.save()

        cls.published_tag.save()
        cls.unpublished_tag.save()

        cls.published_item.clean()
        cls.published_item.save()

        cls.unpublished_item.clean()
        cls.unpublished_item.save()

        cls.published_item.tags.add(cls.published_tag.pk)
        cls.published_item.tags.add(cls.unpublished_tag.pk)

    def test_homepage_context(self):
        response = Client().get(
            reverse("homepage:main"),
        )
        self.assertIn("items", response.context)

    def test_homepage_items(self):
        response = Client().get(
            reverse("homepage:main"),
        )
        items = response.context["items"]
        self.assertEqual(len(items), 0)

    def test_homepage_types(self):
        response = Client().get(
            reverse("homepage:main"),
        )
        self.assertIsInstance(response.context, list)

    @parameterized.parameterized.expand(
        ("is_published",),
    )
    def test_prefetch(self, field_name):
        response = self.client.get(reverse("catalog:main"))
        tag = (
            response.context["items"]
            .first()
            ._prefetched_objects_cache["tags"]
            .first()
        )
        self.assertQuerySetEqual(
            tag.__dict__,
            ["_state", "id", "name"],
            msg="bruh",
        )


class StaticURLTest(TestCase):
    def test_catalog_items_endpoint(self):
        status_code = Client().get(reverse("catalog:main")).status_code
        self.assertEqual(status_code, HTTPStatus.OK)

    @parameterized.parameterized.expand(
        [
            ("/catalog/10/", 404),
            ("/catalog/1.5/", 404),
            ("/catalog/-1/", 404),
            ("/catalog/0/", 404),
            ("/catalog/-0/", 404),
            ("/catalog/10/", 404),
        ],
    )
    def test_catalog_item_endpoint(self, endpoint, error_code):
        response = Client().get(endpoint)
        self.assertEqual(response.status_code, error_code)


class RegexEndpointTest(TestCase):

    @parameterized.parameterized.expand(
        [
            ("/catalog/re/invalid/", None, 404),
            ("/catalog/re/121/", "121", 200),
            ("/catalog/re/asd/", None, 404),
            ("/catalog/re/-12/", None, 404),
            ("/catalog/re/0/", None, 404),
            ("/catalog/re/-0/", None, 404),
        ],
    )
    def test_regex_endpoint(self, endpoint, message, error_code):
        response = self.client.get(endpoint)
        self.assertEqual(response.status_code, error_code)
        if message:
            self.assertEqual(response.content.decode(), message)


class ConverterEndpointTest(TestCase):
    @parameterized.parameterized.expand(
        [
            ("/catalog/converter/invalid/", None, 404),
            ("/catalog/converter/121/", "121", 200),
            ("/catalog/converter/asd/", None, 404),
            ("/catalog/converter/-12/", None, 404),
            ("/catalog/converter/0/", None, 404),
            ("/catalog/converter/-0/", None, 404),
        ],
    )
    def test_converter_endpoint(self, endpoint, message, error_code):
        response = self.client.get(endpoint)
        self.assertEqual(response.status_code, error_code)
        if message:
            self.assertEqual(response.content.decode(), message)


class DBItemTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.category = catalog.models.Category.objects.create(
            name="Test",
            slug="Test",
        )
        cls.tag = catalog.models.Tag.objects.create(
            name="Test",
            slug="Test",
        )

    @parameterized.parameterized.expand(
        [
            ("test", "превосходно", True),
            ("test", "роскошно", True),
            ("test", "Я превосходно", True),
            ("test", "превосходно Я", True),
            ("test", "превосходно роскошно", True),
            ("test", "роскошно!", True),
            ("test", "!роскошно", True),
            ("test", "!роскошно", True),
            ("test", "роскошно©", True),
            ("test", "превосходноН", False),
            ("test", "превНосходно", False),
            ("test", "Нпревосходно", False),
            ("test", "Я превосх%одно", False),
            ("test", "превосходнороскошно", False),
            ("test" * 38, "превосходно", False),
        ],
    )
    def test_add_item(self, name, text, is_validate):
        item_count = catalog.models.Item.objects.count()
        self.item = catalog.models.Item(
            name=name,
            text=text,
            category=self.category,
        )
        if not is_validate:
            with self.assertRaises(ValidationError):
                self.item.full_clean()
                self.item.save()
                self.item.tags.add(self.tag)
                self.item.full_clean()
                self.item.save()
            self.assertEqual(
                catalog.models.Item.objects.count(),
                item_count,
                msg="Validation error",
            )
        else:
            self.item.full_clean()
            self.item.save()
            self.item.tags.add(self.tag)
            self.item.full_clean()
            self.item.save()
            self.assertEqual(
                catalog.models.Item.objects.count(),
                item_count + 1,
                msg="Validation error",
            )


class DBTagTests(TestCase):
    @parameterized.parameterized.expand(
        [
            ("test", "abs", True),
            ("test", "1abs2", True),
            ("test", "a12bs", True),
            ("test", "ABS", True),
            ("test", "-abs-", True),
            ("test", "_abs_", True),
            ("test", "Я", False),
            ("test", "Яabs", False),
            ("test", "Я abs", False),
            ("test", "aЯbs", False),
            ("test", "absЯ", False),
            ("test", "abs Я", False),
            ("test", "*abs*", False),
            ("test", "a*bs", False),
            ("test" * 38, "abs", False),
            ("test", "abs" * 67, False),
        ],
    )
    def test_add_item(self, name, slug, is_validate):
        item_count = catalog.models.Tag.objects.count()
        self.item = catalog.models.Tag(
            name=name,
            slug=slug,
        )
        if not is_validate:
            with self.assertRaises(ValidationError):
                self.item.full_clean()
                self.item.save()
            self.assertEqual(
                catalog.models.Item.objects.count(),
                item_count,
                msg="add no validate item",
            )
        else:
            self.item.full_clean()
            self.item.save()
            self.assertEqual(
                catalog.models.Tag.objects.count(),
                item_count + 1,
                msg="no add validate item",
            )


class CategoryTests(TestCase):
    @parameterized.parameterized.expand(
        [
            ("test", "abs", 1, True),
            ("test", "1abs2", 1, True),
            ("test", "a12bs", 1, True),
            ("test", "ABS", 1, True),
            ("test", "-abs-", 1, True),
            ("test", "_abs_", 1, True),
            ("test", "_abs_", 32767, True),
            ("test", "Я", 1, False),
            ("test", "Яabs", 1, False),
            ("test", "Я abs", 1, False),
            ("test", "aЯbs", 1, False),
            ("test", "absЯ", 1, False),
            ("test", "abs Я", 1, False),
            ("test", "*abs*", 1, False),
            ("test", "a*bs", 1, False),
            ("test" * 38, "abs", 1, False),
            ("test", "abs" * 67, 1, False),
            ("test", "abs", 32768, False),
            ("test", "abs", 0, False),
            ("test", "abs", -1, False),
        ],
    )
    def test_add_item(self, name, slug, weight, is_validate):
        item_count = catalog.models.Category.objects.count()
        self.item = catalog.models.Category(
            name=name,
            slug=slug,
            weight=weight,
        )
        if not is_validate:
            with self.assertRaises(ValidationError):
                self.item.full_clean()
                self.item.save()
            self.assertEqual(
                catalog.models.Item.objects.count(),
                item_count,
                msg="validation error",
            )
        else:
            self.item.full_clean()
            self.item.save()
            self.assertEqual(
                catalog.models.Category.objects.count(),
                item_count + 1,
                msg="validation error",
            )
