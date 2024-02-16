from http import HTTPStatus

from django.test import Client, TestCase


class StaticURLTests(TestCase):
    def test_catalog_items_endpoint(self):
        status_code = Client().get("/catalog/").status_code
        self.assertEqual(status_code, HTTPStatus.OK)

    def test_catalog_item_endpoint(self):
        status_code = Client().get("/catalog/2/").status_code
        self.assertEqual(status_code, HTTPStatus.OK)
        status_code = Client().get("/catalog/abs/").status_code
        self.assertEqual(status_code, HTTPStatus.NOT_FOUND)

    def test_catalog_item_re_endpoint(self):
        status_code = Client().get("/catalog/re/33/").status_code
        self.assertEqual(status_code, HTTPStatus.OK)
        status_code = Client().get("/catalog/re/abc/").status_code
        self.assertEqual(status_code, HTTPStatus.NOT_FOUND)
        status_code = Client().get("/catalog/re/-23/").status_code
        self.assertEqual(status_code, HTTPStatus.NOT_FOUND)
        status_code = Client().get("/catalog/re/22.3333/").status_code
        self.assertEqual(status_code, HTTPStatus.NOT_FOUND)
        status_code = Client().get("/catalog/re/22a22/").status_code
        self.assertEqual(status_code, HTTPStatus.NOT_FOUND)
        status_code = Client().get("/catalog/re/0/").status_code
        self.assertEqual(status_code, HTTPStatus.NOT_FOUND)

    def test_catalog_item_converter_endpoint(self):
        status_code = Client().get("/catalog/converter/33/").status_code
        self.assertEqual(status_code, HTTPStatus.OK)
        status_code = Client().get("/catalog/converter/abc/").status_code
        self.assertEqual(status_code, HTTPStatus.NOT_FOUND)
        status_code = Client().get("/catalog/converter/-23/").status_code
        self.assertEqual(status_code, HTTPStatus.NOT_FOUND)
        status_code = Client().get("/catalog/converter/22.3333/").status_code
        self.assertEqual(status_code, HTTPStatus.NOT_FOUND)
        status_code = Client().get("/catalog/converter/22a22/").status_code
        self.assertEqual(status_code, HTTPStatus.NOT_FOUND)
        status_code = Client().get("/catalog/converter/0/").status_code
        self.assertEqual(status_code, HTTPStatus.NOT_FOUND)
