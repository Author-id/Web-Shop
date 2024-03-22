import django.contrib.auth.backends

import users.models

__all__ = [
    "UserModelBackend",
]


class UserModelBackend(django.contrib.auth.backends.ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        user_model = users.models.User

        user = user_model.objects.get_by_natural_key(username)

        if not user:
            return None

        if user.check_password(password) and self.user_can_authenticate(user):
            if hasattr(user, "profile"):
                user.profile.auth_attempts = 0
                user.profile.save()

            return user

        if hasattr(user, "profile"):
            user.profile.auth_attempts += 1
            user.profile.save()

        return None
