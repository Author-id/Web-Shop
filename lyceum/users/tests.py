import datetime
from unittest.mock import patch

from django.contrib.auth.models import User
from django.test import override_settings
from django.urls import reverse
from django.utils import timezone


__all__ = []


@override_settings(DEFAULT_USER_IS_ACTIVE=False)
def test_user_activation_positive(self):
    self.assertFalse(User.objects.exists())
    self.client.post(
        reverse("users:signup"),
        data={
            "username": "test_username",
            "password1": "VeryStr0ngPa$$",
            "password2": "VeryStr0ngPa$$",
        },
    )
    self.assertFalse(User.objects.first().is_active)
    self.client.get(reverse("users:activate", args=["test_username"]))
    self.assertTrue(User.objects.first().is_active)


@override_settings(DEFAULT_USER_IS_ACTIVE=False)
def test_user_activation_negative(self):
    self.assertFalse(User.objects.exists())
    self.client.post(
        reverse("users:signup"),
        data={
            "username": "test_username",
            "password1": "VeryStr0ngPa$$",
            "password2": "VeryStr0ngPa$$",
        },
    )
    self.assertFalse(User.objects.first().is_active)
    expired_dt = timezone.now() + datetime.timedelta(hours=13)
    with patch("django.utils.timezone.now") as mocked_timezone:
        mocked_timezone.return_value = expired_dt
        self.client.get(reverse("users:activate", args=["test_username"]))
        self.assertFalse(User.objects.first().is_active)


def test_user_signup_positive(self):
    self.assertFalse(User.objects.exists())
    self.client.post(
        reverse("users:signup"),
        data={
            "username": "test_username",
            "password1": "VeryStr0ngPa$$",
            "password2": "VeryStr0ngPa$$",
        },
    )
    self.assertTrue(User.objects.exists())
    self.assertEqual(User.objects.first().username, "test_username")


def test_user_signup_negative(self):
    self.assertFalse(User.objects.exists())
    self.client.post(
        reverse("users:signup"),
        data={
            "username": "test_username",
            "password1": "simple",
            "password2": "simple",
        },
    )
    self.assertFalse(User.objects.exists())
