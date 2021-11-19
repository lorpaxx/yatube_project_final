# from django.contrib.auth import get_user_model
from django.test import TestCase, Client


class CoreViewsTests(TestCase):
    '''
    Тестируем функции приложения core.
    '''
    def setUp(self):
        '''
        Создаём клиента для каждого из тестов.
        '''
        self.guest_client = Client()

    def test_core_views_404(self):
        '''
        Проверяем реакцию на несуществующую страницу (404).
        '''
        test_url = '/hgjkfkjg/'
        template = 'core/404.html'
        response = self.guest_client.get(test_url)
        self.assertEqual(
            response.status_code, 404,
            'Тест не пройден, возвращается не ошибка 404'
        )
        self.assertTemplateUsed(
            response, template,
            'Тест не пройден, не тот шаблон возвращается'
        )
