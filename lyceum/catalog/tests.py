from http import HTTPStatus

from django.test import Client, TestCase


class StaticURLTests(TestCase):
    def test_catalog_endpoint(self):
        response = Client().get("/catalog/")
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_catalog_item_id_endpoint(self):
        response = Client().get("/catalog/777/")
        self.assertEqual(response.status_code, HTTPStatus.OK)
        response = Client().get("/catalog/xxx/")
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
