from django.test import Client, TestCase
from django.urls import reverse
import parameterized

from feedback.forms import FeedbackForm
from feedback.models import Feedback

__all__ = []


class FormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.form = FeedbackForm()

    def test_form_errors(self):
        response = self.client.post(
            reverse("feedback:feedback"),
            data={"text": "YYYAAA", "mail": "unxdd"},
        )
        form = response.context["form"]
        self.assertFalse(form.is_valid())
        self.assertFormError(
            form,
            "mail",
            "Введите правильный адрес электронной почты.",
        )

    def test_name_label(self):
        label_mail = FormTests.form.fields["mail"].label
        label_text = FormTests.form.fields["text"].label
        self.assertEqual(label_mail, "Почта")
        self.assertEqual(label_text, "Текст")

    def test_help_text(self):
        text_help_text = FormTests.form.fields["text"].help_text
        mail_help_text = FormTests.form.fields["mail"].help_text
        self.assertEqual(text_help_text, "Напишите текст письма")
        self.assertEqual(mail_help_text, "Введите почту")

    @parameterized.parameterized.expand(
        [
            (
                {
                    "name": "Ivan4ik",
                    "mail": "ivkaziev@yandex.ru",
                    "text": "asdasdasd",
                },
            ),
            ({"name": "relax", "mail": "un@xdd.ru", "text": "WAWA"},),
        ],
    )
    def test_redirect(self, form_data):
        response = Client().post(
            reverse("feedback:feedback"),
            data=form_data,
            follow=True,
        )
        self.assertIn("form", response.context)
        self.assertRedirects(response, reverse("feedback:feedback"))

    @parameterized.parameterized.expand(
        [
            (
                {
                    "text": "I'm just testing this shit",
                    "name": "",
                    "mail": "recrent@legenda.com",
                },
            ),
            (
                {
                    "text": "Ай-ай-ай-ай-ай-ай-ай убили негра",
                    "name": "Vasya",
                    "mail": "who@ya.com",
                },
            ),
        ],
    )
    def test_from(self, data):
        with self.subTest(data=data):
            feedback_count = Feedback.objects.count()
            response = self.client.post(
                reverse("feedback:feedback"),
                data=data,
                follow=True,
            )

            self.assertRedirects(response, reverse("feedback:feedback"))
            self.assertEqual(
                Feedback.objects.count(),
                feedback_count + 1,
                "Feedback not created",
            )
            self.assertTrue(
                Feedback.objects.filter(
                    mail=data["mail"],
                    name=data["name"] or None,
                    text=data["text"],
                ).exists(),
                "Created incorrect feedback",
            )
