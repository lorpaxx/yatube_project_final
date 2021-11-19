from django.shortcuts import render


def page_not_found(request, exception):
    '''
    Выводит ответ на неизвестную страницу (404).
    '''
    return render(request, 'core/404.html', {'path': request.path}, status=404)


def csrf_failure(request, reason=''):
    '''
    Не был отправлен csrf token (403).
    '''
    return render(request, 'core/403csrf.html')


def server_error(request):
    '''
    Ошибка на сервере (500).
    '''
    return render(request, 'core/500.html', status=500)


def permission_denied(request, exception):
    '''
    Доступ запрещён (403)
    '''
    return render(request, 'core/403.html', status=403)
