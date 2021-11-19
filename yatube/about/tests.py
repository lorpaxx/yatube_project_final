from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from http import HTTPStatus


User = get_user_model()


class AboutURLTests(TestCase):
    '''
    Тестируем URL приложения about.
    '''
    @classmethod
    def setUpClass(cls):
        '''
        Создаём юзера.
        '''
        super().setUpClass()
        cls.user = User.objects.create_user(username='NoName')

    def setUp(self):
        '''
        Создаём клиента для каждого из тестов.
        '''
        self.guest_client = Client()

        self.authorized_client = Client()
        self.authorized_client.force_login(AboutURLTests.user)

    def test_about_url_exist_anonimus_user(self):
        '''
        Проверяем доступность URL для анонимного пользователя.
        '''
        verifiable_URLs = (
            '/about/author/',
            '/about/tech/'
        )
        for verifiable_URL in verifiable_URLs:
            with self.subTest(verifiable_URL=verifiable_URL):
                response = self.guest_client.get(verifiable_URL)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_about_url_exist_authorized_client(self):
        '''
        Проверяем доступность URL для пользователя.
        '''
        verifiable_URLs = (
            '/about/author/',
            '/about/tech/'
        )
        for verifiable_URL in verifiable_URLs:
            with self.subTest(verifiable_URL=verifiable_URL):
                response = self.authorized_client.get(verifiable_URL)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_about_views_pages_use_correct_template(self):
        '''
        Проверяем, что views используют верные шаблоны.
        '''
        posts_templates = {
            reverse('about:author'): 'about/author.html',
            reverse('about:tech'): 'about/tech.html',

        }
        for reverse_name, template in posts_templates.items():
            with self.subTest(template=template):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)
