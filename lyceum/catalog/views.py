from django.http import HttpResponse


def item_list(request):
    return HttpResponse("<body>Список элементов</body>")


def item_detail(request, pk):
    return HttpResponse("<body>Подробно элемент</body>")


def item_detail_re(request, pk):
    return HttpResponse(str(pk))


def item_detail_converter(request, pk):
    return HttpResponse(str(pk))
