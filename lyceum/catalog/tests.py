from http import HTTPStatus

from django.test import Client, TestCase
import parameterized


class StaticURLTests(TestCase):
    def test_endpoint(self):
        response = Client().get("/catalog/")
        self.assertEqual(response.status_code, 200)

    @parameterized.parameterized.expand(
        [
            ("0", 200),
            ("1", 200),
            ("2", 200),
            ("3", 200),
            ("02934890823489423", 200),
            ("-1", 404),
            ("-0293817465", 404),
            ("-", 404),
            ("+", 404),
            ("a", 404),
            ("abcde", 404),
            ("-+_abdce_+-", 404),
            ("777/", 404),
            ("%*^!@#$()", 404),
        ]
    )
    def test_catalog_item_detail_endpoint(self, url, correct_status_code):
        response = Client().get(f"/catalog/{url}/")
        self.assertEqual(response.status_code, correct_status_code)

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
