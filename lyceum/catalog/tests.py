from http import HTTPStatus

from django.test import TestCase, Client


class StaticURLTests(TestCase):
    def test_catalog_items_endpoint(self):
        status_code = Client().get("/catalog/").status_code
        self.assertEqual(status_code, HTTPStatus.OK)

    def test_catalog_item_endpoint(self):
        status_code = Client().get("/catalog/2/").status_code
        self.assertEqual(status_code, HTTPStatus.OK)
        status_code = Client().get("/catalog/abs/").status_code
        self.assertEqual(status_code, HTTPStatus.NOT_FOUND)


