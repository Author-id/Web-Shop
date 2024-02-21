from http import HTTPStatus
import itertools

import django.core.exceptions
from django.test import Client, TestCase

import parameterized

import catalog.models


class StaticURLTests(TestCase):
    def test_catalog_items_endpoint(self):
        status_code = Client().get("/catalog/").status_code
        self.assertEqual(status_code, HTTPStatus.OK)

    @parameterized.parameterized.expand(
        [
            ("0", HTTPStatus.OK),
            ("1", HTTPStatus.OK),
            ("01", HTTPStatus.OK),
            ("010", HTTPStatus.OK),
            ("10", HTTPStatus.OK),
            ("100", HTTPStatus.OK),
            ("abs", HTTPStatus.NOT_FOUND),
            ("a4s", HTTPStatus.NOT_FOUND),
            ("ab4", HTTPStatus.NOT_FOUND),
            ("4ab", HTTPStatus.NOT_FOUND),
            ("4.323", HTTPStatus.NOT_FOUND),
            ("22^1", HTTPStatus.NOT_FOUND),
            ("$221", HTTPStatus.NOT_FOUND),
            ("221%", HTTPStatus.NOT_FOUND),
            ("-0", HTTPStatus.NOT_FOUND),
            ("-1", HTTPStatus.NOT_FOUND),
        ],
    )
    def test_catalog_item_endpoint(self, param, expected_status):
        respone_status_code = Client().get(f"/catalog/{param}/").status_code
        self.assertEqual(
            respone_status_code,
            expected_status,
            msg=f"/catalog/{param}/ get not {expected_status}",
        )

    @parameterized.parameterized.expand(
        (
            (x[0], x[1][0], x[1][1])
            for x in itertools.product(
                [
                    "re",
                    "converter",
                ],
                [
                    ("1", HTTPStatus.OK),
                    ("10", HTTPStatus.OK),
                    ("100", HTTPStatus.OK),
                    ("01", HTTPStatus.NOT_FOUND),
                    ("010", HTTPStatus.NOT_FOUND),
                    ("0", HTTPStatus.NOT_FOUND),
                    ("-0", HTTPStatus.NOT_FOUND),
                    ("-1", HTTPStatus.NOT_FOUND),
                    ("abs", HTTPStatus.NOT_FOUND),
                    ("a4s", HTTPStatus.NOT_FOUND),
                    ("ab4", HTTPStatus.NOT_FOUND),
                    ("4ab", HTTPStatus.NOT_FOUND),
                    ("4.323", HTTPStatus.NOT_FOUND),
                    ("22^1", HTTPStatus.NOT_FOUND),
                    ("$221", HTTPStatus.NOT_FOUND),
                    ("221%", HTTPStatus.NOT_FOUND),
                ],
            )
        ),
    )
    def test_catalog_item_re_converter_endpoint(
        self,
        prefix,
        param,
        expected_status,
    ):
        respone_status_code = (
            Client().get(f"/catalog/{prefix}/{param}/").status_code
        )
        self.assertEqual(
            respone_status_code,
            expected_status,
            msg=f"/catalog/{prefix}/{param}/ get not {expected_status}",
        )


class ModelsItemTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.category = catalog.models.Category.objects.create(
            is_published=True,
            name="try_test",
            slug="slug_slug",
            weight=61,
        )
        cls.tag = catalog.models.Tag.objects.create(
            is_published=True,
            name="tag",
            slug="slug_tag",
        )

    def test_error(self):
        item_count = catalog.models.Item.objects.count()
        with self.assertRaises(django.core.exceptions.ValidationError):
            self.item = catalog.models.Item(
                name="test",
                is_published=True,
                category=self.category,
                text="ничего не работает",
            )
            self.item.full_clean()
            self.item.save()
            self.item.tag.add(self.tag)
        self.assertEqual(
            catalog.models.Item.objects.count(),
            item_count,
        )

    def test_add(self):
        item_count = catalog.models.Item.objects.count()
        self.item = catalog.models.Item(
            is_published=True,
            name="name",
            category=self.category,
            text="роскошно и превосходно",
        )
        self.item.full_clean()
        self.item.save()
        self.item.tags.add(self.tag)
        self.assertEqual(
            catalog.models.Item.objects.count(),
            item_count + 1,
        )


class ModelsTagsTest(TestCase):
    def test_tag(self):
        item_count = catalog.models.Tag.objects.count()
        with self.assertRaises(django.core.exceptions.ValidationError):
            self.item = catalog.models.Tag(
                name="test",
                is_published=True,
                slug="робот",
            )
            self.item.full_clean()
            self.item.save()
        self.assertEqual(
            catalog.models.Tag.objects.count(),
            item_count,
        )

    def test_create(self):
        item_count = catalog.models.Tag.objects.count()
        self.item = catalog.models.Tag(
            is_published=True,
            name="name",
            slug="slug",
        )
        self.item.full_clean()
        self.item.save()
        self.assertEqual(
            catalog.models.Tag.objects.count(),
            item_count + 1,
        )


class ModelsCategoryTest(TestCase):
    def test_category(self):
        item_count = catalog.models.Category.objects.count()
        with self.assertRaises(django.core.exceptions.ValidationError):
            self.item = catalog.models.Category(
                name="test",
                is_published=True,
                slug="робот",
                weight=45,
            )
            self.item.full_clean()
            self.item.save()
        self.assertEqual(
            catalog.models.Category.objects.count(),
            item_count,
        )

    def test_create_category(self):
        item_count = catalog.models.Category.objects.count()
        self.item = catalog.models.Category(
            name="name",
            is_published=True,
            slug="sllug123",
            weight=45,
        )
        self.item.full_clean()
        self.item.save()
        self.assertEqual(
            catalog.models.Category.objects.count(),
            item_count + 1,
        )
