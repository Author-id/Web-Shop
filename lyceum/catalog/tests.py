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

    def test_catalog_re_item_id_endpoint(self):
        response = Client().get("/catalog/re/777/")
        self.assertEqual(response.status_code, HTTPStatus.OK)
        response = Client().get("/catalog/re/1/")
        self.assertEqual(response.status_code, HTTPStatus.OK)
        response = Client().get("/catalog/re/xxx/")
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        response = Client().get("/catalog/re/0/")
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        response = Client().get("/catalog/re/-1/")
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        response = Client().get("/catalog/re/5.5/")
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_catalog_converter_item_id_endpoint(self):
        response = Client().get("/catalog/converter/777")
        self.assertEqual(response.status_code, HTTPStatus.OK)
        response = Client().get("/catalog/converter/1")
        self.assertEqual(response.status_code, HTTPStatus.OK)
        response = Client().get("/catalog/converter/xxx/")
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        response = Client().get("/catalog/converter/0/")
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        response = Client().get("/catalog/converter/-1/")
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        response = Client().get("/catalog/converter/5.5/")
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
