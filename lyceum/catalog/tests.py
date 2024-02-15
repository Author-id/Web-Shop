from http import HTTPStatus

from django.test import Client, TestCase


class StaticURLTests(TestCase):
    def test_item_list_endpoint(self):
        resp = Client().get("/catalog/")
        self.assertEqual(resp.status_code, HTTPStatus.OK)

    def test_item_detail_endpoint(self):
        resp = Client().get("/catalog/3")
        self.assertEqual(resp.status_code, HTTPStatus.OK)

        resp = Client().get("/catalog/string/")
        self.assertEqual(resp.status_code, HTTPStatus.NOT_FOUND)
