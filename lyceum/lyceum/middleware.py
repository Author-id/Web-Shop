import re

from django.conf import settings


class ReverseMiddleware:
    count = 0

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if self.__class__.count == 9:
            if settings.ALLOW_REVERSE:
                content = response.content.decode("utf-8")
                russian_words = re.findall("[а-яА-ЯёЁ]+", content)
                for word in russian_words:
                    content = content.replace(word, word[::-1])
                response.content = content.encode("utf-8")
            self.__class__.count = 0
            return response
        self.__class__.count += 1
        return response

    def reverse_russki(self, text):
        abc = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
        result = []
        for word in text.split():
            for letter in word.lower():
                if letter not in abc:
                    result.append(word)
                    break
            else:
                result.append(word[::-1])

        return " ".join(result)
