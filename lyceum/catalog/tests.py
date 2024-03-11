from http import HTTPStatus
import itertools

from django.core.exceptions import ValidationError
from django.test import Client, TestCase
from django.urls import reverse
import parameterized

import catalog.models

__all__ = []


class StaticURLTests(TestCase):
    def test_catalog_items_endpoint(self):
        status_code = Client().get(reverse("catalog:main")).status_code
        self.assertEqual(status_code, HTTPStatus.OK)

    def test_catalog_friday_endpoint(self):
        status_code = Client().get(reverse("catalog:friday")).status_code
        self.assertEqual(status_code, HTTPStatus.OK)

    def test_catalog_new_endpoint(self):
        status_code = Client().get(reverse("catalog:new")).status_code
        self.assertEqual(status_code, HTTPStatus.OK)

    def test_catalog_unverified_endpoint(self):
        status_code = Client().get(reverse("catalog:unverified")).status_code
        self.assertEqual(status_code, HTTPStatus.OK)


class DBItemTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.category = catalog.models.Category.objects.create(
            name="Test",
        )
        cls.tag = catalog.models.Tag.objects.create(
            name="Test",
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
                msg="add no validate item",
            )
        else:
            self.item.full_clean()
            self.item.save()
            self.item.tags.add(self.tag)
            self.assertEqual(
                catalog.models.Item.objects.count(),
                item_count + 1,
                msg="no add validate item",
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
    def test_add_tag(self, name, slug, is_validate):
        tag_count = catalog.models.Tag.objects.count()
        self.tag = catalog.models.Tag(
            name=name,
            slug=slug,
        )
        if not is_validate:
            with self.assertRaises(ValidationError):
                self.tag.full_clean()
                self.tag.save()

            self.assertEqual(
                catalog.models.Item.objects.count(),
                tag_count,
                msg="add no validate item",
            )
        else:
            self.tag.full_clean()
            self.tag.save()
            self.assertEqual(
                catalog.models.Tag.objects.count(),
                tag_count + 1,
                msg="no add validate item",
            )


class DBCategoryTests(TestCase):
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
    def test_add_category(
        self,
        name,
        slug,
        weight,
        is_validate,
    ):
        category_count = catalog.models.Category.objects.count()
        self.category = catalog.models.Category(
            name=name,
            slug=slug,
            weight=weight,
        )
        if not is_validate:
            with self.assertRaises(ValidationError):
                self.category.full_clean()
                self.category.save()

            self.assertEqual(
                catalog.models.Item.objects.count(),
                category_count,
                msg="add no validate item",
            )
        else:
            self.category.full_clean()
            self.category.save()
            self.assertEqual(
                catalog.models.Category.objects.count(),
                category_count + 1,
                msg="no add validate item",
            )


class DBNormalizeNameTests(TestCase):
    @parameterized.parameterized.expand(
        (
            (test_value[0], *test_value[1])
            for test_value in itertools.product(
                [
                    ("test"),
                    ("Тest"),
                    ("tЕst"),
                ],
                [
                    ("test test", True),
                    ("itfaketest", True),
                    ("test, test", True),
                    ("test!test", True),
                    ("testt", True),
                    ("test!", False),
                    ("!test", False),
                    ("!test!", False),
                    (" test ", False),
                    ("test,", False),
                    (".test", False),
                    ("te st", False),
                    ("te sТ", False),
                    ("tеst", False),
                ],
            )
        ),
    )
    def test_add_tag(self, name1, name2, is_validate):
        tag_count = catalog.models.Category.objects.count()
        self.tag1 = catalog.models.Tag(
            name=name1,
        )
        self.tag2 = catalog.models.Tag(
            name=name2,
        )
        if not is_validate:
            with self.assertRaises(
                ValidationError,
                msg=f"add {name2} but we have {name1}",
            ):
                self.tag1.full_clean()
                self.tag1.save()
                self.tag2.full_clean()
                self.tag2.save()

            self.assertEqual(
                catalog.models.Tag.objects.count(),
                tag_count + 1,
                msg="add no validate item",
            )
        else:
            self.tag1.full_clean()
            self.tag1.save()
            self.tag2.full_clean()
            self.tag2.save()
            self.assertEqual(
                catalog.models.Tag.objects.count(),
                tag_count + 2,
                msg="no add validate item",
            )


class CatalogContentTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.category_published = catalog.models.Category.objects.create(
            is_published=True,
            name="Тестовая опубликованная категория",
            slug="published-category",
        )
        cls.category_published.full_clean()
        cls.category_published.save()

        cls.tag_published = catalog.models.Tag.objects.create(
            is_published=True,
            name="Тестовый опубликованный тег",
            slug="published-tag",
        )
        cls.tag_published.full_clean()
        cls.tag_published.save()

        cls.item_published = catalog.models.Item.objects.create(
            is_published=True,
            name="Тестовый опубликованный предмет",
            text="превосходно",
            category=cls.category_published,
        )
        cls.item_published.full_clean()
        cls.item_published.save()

        cls.item_on_main = catalog.models.Item.objects.create(
            is_published=True,
            is_on_main=True,
            name="Тестовый предмет на главной странице",
            text="превосходно",
            category=cls.category_published,
        )
        cls.item_on_main.full_clean()
        cls.item_on_main.save()

        cls.item_unpublished = catalog.models.Item.objects.create(
            is_published=False,
            name="Тестовый неопубликованный предмет",
            text="превосходно",
            category=cls.category_published,
        )

        cls.item_unpublished.full_clean()
        cls.item_unpublished.save()

        cls.item_published.tags.add(cls.tag_published)
        cls.item_on_main.tags.add(cls.tag_published)
        cls.item_published.tags.add(cls.tag_published)

    def test_home_page_correct_context(self):
        response = self.client.get(reverse("homepage:main"))
        self.assertIn("items", response.context)

    def test_item_list_page_correct_context(self):
        response = self.client.get(reverse("catalog:main"))
        self.assertIn("items", response.context)

    def test_home_count_item(self):
        response = self.client.get(reverse("homepage:main"))
        self.assertEqual(len(response.context["items"]), 1)

    def test_item_list_count_item(self):
        response = self.client.get(reverse("catalog:main"))
        self.assertEqual(len(response.context["items"]), 2)

    def test_item_type(self):
        response = self.client.get(reverse("catalog:main"))
        items = response.context["items"]
        self.assertIsInstance(items.first(), catalog.models.Item)

    @parameterized.parameterized.expand(
        (
            "is_published",
            "normalize_name",
            "created",
            "updated",
        ),
    )
    def test_filds_item_main(self, field_name):
        response = self.client.get(reverse("homepage:main"))
        self.assertNotIn(
            field_name,
            response.context["items"].first().__dict__,
            msg=f"find useless field '{field_name}' in main query",
        )

    @parameterized.parameterized.expand(
        (
            "is_published",
            "normalize_name",
            "created",
            "updated",
        ),
    )
    def test_filds_item_list(self, field_name):
        response = self.client.get(reverse("catalog:main"))
        self.assertNotIn(
            field_name,
            response.context["items"].first().__dict__,
            msg=f"find useless field '{field_name}' in main query",
        )

    def test_filds_tags_main(self):
        correct_fields = [
            "_state",
            "id",
            "name",
        ]
        response = self.client.get(reverse("homepage:main"))
        item = response.context["items"].first()
        tag = item._prefetched_objects_cache["tags"].first()
        self.assertQuerySetEqual(
            tag.__dict__,
            correct_fields,
            msg="not correct use field in main item.tags query",
        )
