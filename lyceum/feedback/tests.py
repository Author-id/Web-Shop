from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse

import feedback.models


__all__ = []


class PostMethodTest(TestCase):
    def test_form_errors(self):
        response = self.client.post(
            reverse("feedback:feedback"),
            data={"text": "some test text", "mail": "not an email"},
        )
        form = response.context["form"]
        self.assertFalse(form.is_valid())
        self.assertFormError(
            form,
            "mail",
            "Введите правильный адрес электронной почты.",
        )

    def test_form_in_context(self):
        response = self.client.get(reverse("feedback:feedback"))
        self.assertIn("form", response.context)

    def test_form_labels(self):
        response = self.client.get(reverse("feedback:feedback"))
        form = response.context["form"]
        self.assertEqual(form.fields["text"].label, "Текст")
        self.assertEqual(form.fields["mail"].label, "Почта")

    def test_form_help_texts(self):
        response = self.client.get(reverse("feedback:feedback"))
        form = response.context["form"]
        self.assertEqual(
            form.fields["text"].help_text,
            "напишите текст сообщения",
        )
        self.assertEqual(
            form.fields["mail"].help_text,
            "почтовый адрес",
        )

    def test_submit_redirect(self):
        item_count = feedback.models.Feedback.objects.count()
        response = self.client.post(
            reverse("feedback:feedback"),
            data={
                "name": "test",
                "text": "some test text",
                "mail": "test@test.com",
            },
            follow=True,
        )
        self.assertRedirects(
            response,
            reverse("feedback:feedback"),
            status_code=HTTPStatus.FOUND,
            target_status_code=HTTPStatus.OK,
        )
        self.assertIn("form", response.context)
        form = response.context["form"]
        self.assertEqual(form.fields["text"].label, "Текст")
        self.assertEqual(form.fields["mail"].label, "Почта")
        self.assertEqual(
            feedback.models.Feedback.objects.count(),
            item_count + 1,
        )
        self.assertTrue(
            feedback.models.Feedback.objects.filter(
                mail="test@test.com",
            ).exists(),
        )
