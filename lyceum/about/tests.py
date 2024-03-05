from http import HTTPStatus

from django.test import Client, TestCase
from django.urls import reverse

__all__ = ["StaticURLTest"]


class StaticURLTest(TestCase):
    def test_about_endpoint(self):
        status_code = Client().get(reverse("about:main")).status_code
        self.assertEqual(status_code, HTTPStatus.OK)
