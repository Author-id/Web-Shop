from users.models import UserProxy


class UserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    @staticmethod
    def authenticate(request):
        if request.user.is_authenticated:
            return True

        return False

    def __call__(self, request):
        if hasattr(request, "user") and self.authenticate(request):
            request.user.__class__ = UserProxy

        return self.get_response(request)
