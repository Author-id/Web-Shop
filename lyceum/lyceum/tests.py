from django.test import Client, override_settings, TestCase


class ReverseMiddlewareTests(TestCase):
    @override_settings(ALLOW_REVERSE=True)
    def test_reverse(self):
        rev_c = 0
        for i in range(1, 11):
            response = Client().get("/coffee/")
            if response.content.decode() == "Я кинйач":
                rev_c += 1
        self.assertEqual(rev_c, 1)

    @override_settings(ALLOW_REVERSE=False)
    def test_no_reverse(self):
        for i in range(1, 11):
            response = Client().get("/coffee/")
            self.assertEqual(response.content.decode(), "Я чайник")
