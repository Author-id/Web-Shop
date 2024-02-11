from django.test import TestCase, Client


class StaticURLTests(TestCase):
    def test_about_endpoint(self):
        response = Client().get('/')
        self.assertEqual(response.status_code, 200)
