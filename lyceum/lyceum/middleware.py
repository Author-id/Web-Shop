from django.conf import settings

requests_count = 0


class ReverseMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        global requests_count
        response = self.get_response(request)

        requests_count += 1
        if settings.ALLOW_REVERSE and requests_count % 10 == 0:
            rev_text = self.reverse_russki(response.content.decode())
            response.content = rev_text
            requests_count = 0
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