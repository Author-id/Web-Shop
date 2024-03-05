import re

from django.conf import settings

__all__ = ["ReverseRussianWordsMiddleware"]


class ReverseRussianWordsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        settings.COUNT += 1
        if settings.COUNT % 10 == 0 and settings.ALLOW_REVERSE:
            response.content = self.reverse_russian_words(response.content)
        return response

    def reverse_russian_words(self, content):
        content = content.decode("utf-8")
        words_and_tags = re.findall(r"(<.*?>|\b\w+\b)", content)
        return " ".join(
            word[::-1] if not word.startswith("<") else word
            for word in words_and_tags
        )
