from http import HTTPStatus
import itertools

from django.test import Client, TestCase
import parameterized


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
