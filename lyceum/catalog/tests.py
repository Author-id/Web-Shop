from http import HTTPStatus

from django.test import Client, TestCase


class StaticURLTests(TestCase):
    def test_item_list_endpoint(self):
        resp = Client().get("/catalog/")
        self.assertEqual(resp.status_code, HTTPStatus.OK)

    def test_item_detail_endpoint(self):
        resp = Client().get("/catalog/3/")
        self.assertEqual(resp.status_code, HTTPStatus.OK)

        resp = Client().get("/catalog/string/")
        self.assertEqual(resp.status_code, HTTPStatus.NOT_FOUND)

    def test_re_positive_int_endpoint(self):
        resp = Client().get("/catalog/re/23/")
        self.assertEqual(resp.status_code, HTTPStatus.OK)
        self.assertEqual(resp.content, "23".encode())

        not_founs_urls = [
            "/catalog/re/string/",
            "/catalog/re/23/string/",
            "/catalog/re/-23/",
            "/catalog/re/0/",
        ]

        for url in not_founs_urls:
            resp = Client().get(url)
            self.assertEqual(resp.status_code, HTTPStatus.NOT_FOUND)

    def test_converter_positive_integer_endpoint(self):
        resp = Client().get("/catalog/converter/23/")
        self.assertEqual(resp.status_code, HTTPStatus.OK)
        self.assertEqual(resp.content, "23".encode())

        not_founs_urls = [
            "/catalog/converter/string/",
            "/catalog/converter/23/string/",
            "/catalog/converter/-23/",
            "/catalog/converter/0/",
        ]

        for url in not_founs_urls:
            resp = Client().get(url)
            self.assertEqual(resp.status_code, HTTPStatus.NOT_FOUND)
