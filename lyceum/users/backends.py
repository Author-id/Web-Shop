import re

import django.conf
import django.contrib.auth.backends
import django.contrib.auth.signals
import django.dispatch

import users.models

__all__ = []


class AuthenticationBackend(django.contrib.auth.backends.ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        email_re = r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]"

        if username is None or password is None:
            return None

        if re.match(email_re, username):
            try:
                user = users.models.User.objects.by_mail(username)
            except users.models.User.DoesNotExist:
                return None
        else:
            try:
                user = users.models.User.objects.get(username=username)
            except users.models.User.DoesNotExist:
                return None

        if user.check_password(password) and self.user_can_authenticate(user):
            user.profile.attempts_count = 0
            user.profile.save()
            return user

        user.profile.attempts_count += 1
        user.profile.save()

        if (
            user.profile.attempts_count
            >= django.conf.settings.MAX_AUTH_ATTEMPTS
        ):
            user.is_active = False
            user.profile.block_date = django.utils.timezone.now()
            user.save()
            user.profile.save()

            users.email.send_user_email(
                username,
                user.email,
                "users/reactivate_email.html",
            )

        return None
