import datetime
import unittest.mock

import django.contrib.auth
import django.core.mail
import django.test
import django.urls
import django.utils
import parameterized.parameterized

import users.models


class TestUserSignUp(django.test.TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.client = django.test.Client()
        cls.user_model = django.contrib.auth.get_user_model()
        cls.user = cls.user_model.objects.create_user(
            email="test@example.com",
            password="testpassword",
            username="testuserr",
        )
        cls.user.profile = users.models.Profile.objects.create(
            user_id=cls.user.id,
        )

    @classmethod
    def tearDownClass(cls):
        cls.user_model.objects.all().delete()

        super().tearDownClass()

    def test_signup(self):
        data = {
            "username": "testinguser",
            "email": "testuser@example.com",
            "password1": "testpassword",
            "password2": "testpassword",
        }

        response = self.client.post(
            django.urls.reverse("users:signup"),
            data,
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            django.urls.reverse("users:login"),
        )

        self.assertTrue(
            self.user_model.objects.filter(username="testinguser").exists(),
        )

        user = django.shortcuts.get_object_or_404(
            django.contrib.auth.get_user_model().objects,
            username="testinguser",
        )

        self.assertTrue(
            user.is_authenticated,
        )

    @django.test.override_settings(DEFAULT_USER_IS_ACTIVE=False)
    def test_user_activation_positive(self):
        self.client.post(
            django.urls.reverse("users:signup"),
            data={
                "username": "test_username",
                "password1": "testpassword",
                "password2": "testpassword",
            },
        )
        user = django.shortcuts.get_object_or_404(
            django.contrib.auth.get_user_model().objects,
            username="test_username",
        )
        self.assertFalse(user.is_active)
        self.client.get(
            django.urls.reverse("users:activate", args=["test_username"]),
        )
        user = django.shortcuts.get_object_or_404(
            django.contrib.auth.get_user_model().objects,
            username="test_username",
        )
        self.assertTrue(user.is_active)

    @django.test.override_settings(DEFAULT_USER_IS_ACTIVE=False)
    def test_user_activation_negative(self):
        self.client.post(
            django.urls.reverse("users:signup"),
            data={
                "username": "test_username2",
                "password1": "testpassword",
                "password2": "testpassword",
            },
        )
        expired_dt = django.utils.timezone.now() + datetime.timedelta(hours=13)
        with unittest.mock.patch(
            "django.utils.timezone.now",
        ) as mocked_timezone:
            mocked_timezone.return_value = expired_dt
            self.client.get(
                django.urls.reverse("users:activate", args=["test_username2"]),
            )

        user = django.shortcuts.get_object_or_404(
            django.contrib.auth.get_user_model().objects,
            username="test_username2",
        )

        self.assertFalse(user.is_active)

    def test_sign_up_with_duplicate_emails(self):
        response = self.client.post(
            django.urls.reverse("users:signup"),
            data={
                "username": "testinguser2",
                "email": self.user.email,
                "password1": "testpassword",
                "password2": "testpassword",
            },
        )
        self.assertEqual(response.status_code, 200)  # Редиректа не произошло


class TestUserLogin(django.test.TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.client = django.test.Client()
        cls.user_model = django.contrib.auth.get_user_model()
        cls.user = cls.user_model.objects.create_user(
            email="testing@example.com",
            password="testpassword",
            username="testuser",
        )
        cls.user.profile = users.models.Profile.objects.create(
            user_id=cls.user.id,
        )

    @classmethod
    def tearDownClass(cls):
        cls.user_model.objects.all().delete()

        super().tearDownClass()

    def test_login_by_email(self):
        response = self.client.post(
            django.urls.reverse("users:login"),
            {
                "username": "testing@example.com",
                "password": "testpassword",
            },
        )
        self.assertEqual(response.status_code, 302)

    def test_login_by_username(self):
        response = self.client.post(
            django.urls.reverse("users:login"),
            {
                "username": "testuser",
                "password": "testpassword",
            },
        )
        self.assertEqual(response.status_code, 302)

    def test_login_invalid_credentials(self):
        response = self.client.post(
            django.urls.reverse("users:login"),
            {
                "username": "testign@example.com",
                "password": "wrongpassword",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context["user"].is_authenticated)


class TestUserNormalizeEmail(django.test.TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.client = django.test.Client()
        cls.user_model = django.contrib.auth.get_user_model()

        cls.user = cls.user_model.objects.create_user(
            password="testpassword",
            username="testuser1",
            email="test@gmail.com",
        )
        cls.user.profile = users.models.Profile.objects.create(
            user_id=cls.user.id,
        )

        cls.user2 = cls.user_model.objects.create_user(
            password="testpassword",
            username="testuser2",
            email="tes-t@yandex.ru",
        )
        cls.user2.profile = users.models.Profile.objects.create(
            user_id=cls.user2.id,
        )

    @classmethod
    def tearDownClass(cls):
        cls.user_model.objects.all().delete()

        super().tearDownClass()

    @parameterized.parameterized.expand(
        [
            ".tEs.T+testtag@gmail.com",
            "test+testtag@gmAil.com",
            "test@gmail.com",
            "tEs-T+testtag@yandex.ru",
            "tes.t+testtag@YA.ru",
            "tes-t@ya.ru",
        ],
    )
    def test_login_user_gmail(self, email):
        response = self.client.post(
            django.urls.reverse("users:login"),
            {
                "username": email,
                "password": "testpassword",
            },
        )
        self.assertEqual(response.status_code, 200)


class TestUserDeactivation(django.test.TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.client = django.test.Client()
        cls.user_model = django.contrib.auth.get_user_model()

        cls.user = cls.user_model.objects.create_user(
            password="testpassword",
            username="testuser",
        )
        cls.user.profile = users.models.Profile.objects.create(
            user_id=cls.user.id,
        )

        cls.user2 = cls.user_model.objects.create_user(
            password="testpassword",
            username="testuser2",
        )
        cls.user2.profile = users.models.Profile.objects.create(
            user_id=cls.user2.id,
        )

        cls.user3 = cls.user_model.objects.create_user(
            password="testpassword",
            username="testuser3",
        )
        cls.user3.profile = users.models.Profile.objects.create(
            user_id=cls.user3.id,
        )

    @classmethod
    def tearDownClass(cls):
        cls.user_model.objects.all().delete()

        super().tearDownClass()

    @django.test.override_settings(
        MAX_AUTH_ATTEMPTS=2,
        DEFAULT_USER_IS_ACTIVE=True,
    )
    def test_user_deactivation(self):
        for _ in range(2):
            response = self.client.post(
                django.urls.reverse("users:login"),
                {
                    "username": self.user.username,
                    "password": "wrongpassword",
                },
                follow=True,
            )

            self.assertEqual(response.status_code, 200)
            self.assertFalse(response.context["user"].is_authenticated)

        user = django.shortcuts.get_object_or_404(
            django.contrib.auth.get_user_model().objects,
            username=self.user.username,
        )

        self.assertFalse(user.is_active)

    @django.test.override_settings(
        MAX_AUTH_ATTEMPTS=2,
        DEFAULT_USER_IS_ACTIVE=True,
    )
    def test_user_reactivation_positive(self):
        for _ in range(2):
            self.client.post(  # Deactivate testuser2
                django.urls.reverse("users:login"),
                {
                    "username": self.user2.username,
                    "password": "wrongpassword",
                },
                follow=True,
            )

        user = django.shortcuts.get_object_or_404(
            django.contrib.auth.get_user_model().objects,
            username=self.user2.username,
        )
        self.assertFalse(user.is_active)

        self.client.get(
            django.urls.reverse("users:reactivate", args=["testuser2"]),
        )
        user = django.shortcuts.get_object_or_404(
            django.contrib.auth.get_user_model().objects,
            username="testuser2",
        )
        self.assertTrue(user.is_active)

    @django.test.override_settings(
        MAX_AUTH_ATTEMPTS=2,
        DEFAULT_USER_IS_ACTIVE=True,
    )
    def test_user_reactivation_negative(self):
        for _ in range(2):
            self.client.post(  # Deactivate testuser3
                django.urls.reverse("users:login"),
                {
                    "username": self.user3.username,
                    "password": "wrongpassword",
                },
                follow=True,
            )

        expired_dt = django.utils.timezone.now() + datetime.timedelta(days=8)
        with unittest.mock.patch(
            "django.utils.timezone.now",
        ) as mocked_timezone:
            mocked_timezone.return_value = expired_dt
            self.client.get(
                django.urls.reverse("users:reactivate", args=["testuser3"]),
            )

        user = django.shortcuts.get_object_or_404(
            django.contrib.auth.get_user_model().objects,
            username=self.user3.username,
        )

        self.assertFalse(user.is_active)


__all__ = []
