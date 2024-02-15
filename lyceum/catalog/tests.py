import parameterized
from django.test import Client, TestCase


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
