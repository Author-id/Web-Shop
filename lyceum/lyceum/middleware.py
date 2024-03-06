import re

from django.conf import settings

__all__ = ["ReverseResponseMiddleware"]


class ReverseResponseMiddleware:
    count = 0

    def __init__(
        self,
        get_response,
    ):
        self.get_response = get_response

    @staticmethod
    def reverse_russian_words(content):
        russian_words = re.findall("[а-яА-ЯёЁ]+", content)
        for word in russian_words:
            content = content.replace(word, word[::-1])
        return content

    def __call__(self, request):
        response = self.get_response(request)
        if self.__class__.count == 9:
            if settings.ALLOW_REVERSE:
                content = response.content.decode("utf-8")
                response.content = self.reverse_russian_words(content).encode(
                    "utf-8",
                )
            self.__class__.count = 0
            return response
        self.__class__.count += 1
        return response
