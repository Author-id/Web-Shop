import itertools

from django.core.exceptions import ValidationError
import parameterized
from rest_framework import status
from rest_framework.test import APITestCase

import catalog.models


class StaticUrlTests(APITestCase):
    def test_catalog_endpoint(self):
        response = self.client.get("/catalog/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @parameterized.parameterized.expand(
        [
            ("1", status.HTTP_200_OK),
            ("100", status.HTTP_200_OK),
            ("0", status.HTTP_200_OK),
            ("-0", status.HTTP_404_NOT_FOUND),
            ("-100", status.HTTP_404_NOT_FOUND),
            ("0.5", status.HTTP_404_NOT_FOUND),
            ("abc", status.HTTP_404_NOT_FOUND),
            ("0abc", status.HTTP_404_NOT_FOUND),
            ("abc0", status.HTTP_404_NOT_FOUND),
            ("$%^", status.HTTP_404_NOT_FOUND),
            ("1e5", status.HTTP_404_NOT_FOUND),
        ],
    )
    def test_catalog_item_endpoint(self, url, expected_status):
        response = self.client.get(f"/catalog/{url}/")
        self.assertEqual(response.status_code, expected_status)

    @parameterized.parameterized.expand(
        (
            (x[0], x[1][0], x[1][1])
            for x in itertools.product(
                ["converter", "re"],
                [
                    ("1", status.HTTP_200_OK),
                    ("100", status.HTTP_200_OK),
                    ("0", status.HTTP_200_OK),
                    ("-0", status.HTTP_404_NOT_FOUND),
                    ("-100", status.HTTP_404_NOT_FOUND),
                    ("0.5", status.HTTP_404_NOT_FOUND),
                    ("abc", status.HTTP_404_NOT_FOUND),
                    ("0abc", status.HTTP_404_NOT_FOUND),
                    ("abc0", status.HTTP_404_NOT_FOUND),
                    ("$%^", status.HTTP_404_NOT_FOUND),
                    ("1e5", status.HTTP_404_NOT_FOUND),
                ],
            )
        ),
    )
    def test_catalog_item_pint_endpoint(
        self,
        prefix,
        url,
        expected_status,
    ):
        full_url = f"/catalog/{prefix}/{url}/"
        response = self.client.get(full_url)
        self.assertEqual(
            response.status_code,
            expected_status,
            f"failed check status request to {full_url}",
        )


class DBItemTests(APITestCase):
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
        with self.subTest(name=name, text=text, is_validate=is_validate):
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
                self.item.full_clean()
                self.item.save()
                self.assertEqual(
                    catalog.models.Item.objects.count(),
                    item_count + 1,
                    msg="no add validate item",
                )


class DBTagTests(APITestCase):
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
                catalog.models.Tag.objects.count(),
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


class DBCategoryTests(APITestCase):
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
    def test_add_category(self, name, slug, weight, is_validate):
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
                catalog.models.Category.objects.count(),
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


class DBNormalizeNameTests(APITestCase):
    @parameterized.parameterized.expand(
        (
            (x[0], x[1][:-1], x[1][2])
            for x in itertools.product(
                [
                    ("test", "1"),
                ],
                [
                    ("test test", "2", True),
                    ("itfaketest", "2", True),
                    ("test, test", "2", True),
                    ("test!test", "2", True),
                    ("test!", "2", False),
                    ("!test", "2", False),
                    ("!test!", "2", False),
                    (" test ", "2", False),
                    ("test,", "2", False),
                    (".test", "2", False),
                    ("testt", "2", False),
                    ("te st", "2", False),
                ],
            )
        ),
    )
    def test_add_item(self, data1, data2, is_validate):
        self.tag = catalog.models.Tag(
            name=data1[0],
            slug=data1[1],
        )
        self.tag.full_clean()
        self.tag.save()
        tag_count = catalog.models.Tag.objects.count()
        self.tag = catalog.models.Tag(
            name=data2[0],
            slug=data2[1],
        )
        if not is_validate:
            with self.assertRaises(ValidationError):
                self.tag.full_clean()
                self.tag.save()
            self.assertEqual(
                catalog.models.Tag.objects.count(),
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
