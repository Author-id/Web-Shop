from pathlib import Path
import shutil

from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import override_settings, TestCase
from django.urls import reverse
from django.utils.translation import gettext
from parameterized import parameterized

from feedback.forms import FeedbackAuthorForm, FeedbackFileForm, FeedbackForm
from feedback.models import Feedback


__all__ = [
    "FormTests",
]


MEDIA_TEST: Path = settings.BASE_DIR / "media_test"


class FormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.form = FeedbackForm()
        cls.form_author = FeedbackAuthorForm()

    def test_mail_label(self):
        mail_label = FormTests.form_author.fields["mail"].label
        self.assertEqual(mail_label, "Почта")

    def test_text_label(self):
        text_label = FormTests.form.fields["text"].label
        self.assertEqual(text_label, "Текст")

    def test_mail_help_text(self):
        mail_help_text = FormTests.form_author.fields["mail"].help_text
        self.assertEqual(
            mail_help_text,
            gettext("почтовый адрес"),
        )

    def test_text_help_text(self):
        text_help_text = FormTests.form.fields["text"].help_text
        self.assertEqual(text_help_text, "напишите текст сообщения")

    @parameterized.expand(
        [
            ("form", FeedbackForm),
            ("author_form", FeedbackAuthorForm),
            ("files_form", FeedbackFileForm),
        ],
    )
    def test_feedback_correct_context(
        self,
        form_name,
        form_type,
    ):
        with self.subTest(form_name=form_name, form_type=form_type):
            response = self.client.get(reverse("feedback:feedback"))
            self.assertIn(form_name, response.context)
            form = response.context[form_name]
            self.assertIsInstance(form, form_type)

    @parameterized.expand(
        [
            ({"text": "some text", "name": "", "mail": "test@test.com"},),
            ({"text": "some text", "name": "Vasya", "mail": "test@test.com"},),
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
                    author__mail=data["mail"],
                    author__name=data["name"] or None,
                    text=data["text"],
                ).exists(),
                "Uncorrect feedback created",
            )

    def test_form_errors(self):
        data = {"text": "some text", "mail": "wrong email"}
        feedback_count = Feedback.objects.count()
        response = self.client.post(
            reverse("feedback:feedback"),
            data=data,
            follow=True,
        )
        self.assertFormError(
            response,
            "author_form",
            "mail",
            "Введите правильный адрес электронной почты.",
        )
        self.assertEqual(
            Feedback.objects.count(),
            feedback_count,
            "Feedback created while validation failed",
        )

    @override_settings(MEDIA_ROOT=MEDIA_TEST)
    def test_form_file_upload(self):
        content = "Test file content".encode()
        file_upload = SimpleUploadedFile(
            "file.txt",
            content,
            content_type="text/plain",
        )
        data = {
            "text": "some text",
            "mail": "test@test.com",
            "files": [file_upload],
        }
        feedback_count = Feedback.objects.count()
        response = self.client.post(
            reverse("feedback:feedback"),
            data=data,
            format="multipart",
            follow=True,
        )

        self.assertRedirects(response, reverse("feedback:feedback"))
        self.assertEqual(
            Feedback.objects.count(),
            feedback_count + 1,
            "Feedback not created",
        )
        feedback = Feedback.objects.filter(
            author__mail=data["mail"],
            text=data["text"],
        ).get()
        files = list(feedback.files.all())
        self.assertEqual(len(files), 1, "Wrong count of files created")
        with (MEDIA_TEST / files[0].file.name).open("rb") as f:
            self.assertEqual(f.read(), content, "Wrong file content")

    @classmethod
    def tearDownClass(cls):
        super().setUpClass()
        shutil.rmtree(MEDIA_TEST)
