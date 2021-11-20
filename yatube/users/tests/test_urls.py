from django.contrib.auth import get_user_model
from django.test import TestCase, Client

from http import HTTPStatus


User = get_user_model()


class UsersURLTests(TestCase):
    '''
    Тестируем URL приложения users.
    '''
    @classmethod
    def setUpClass(cls):
        '''
        Создаём записи в БД.
        '''
        super().setUpClass()
        cls.user = User.objects.create_user(username='NoName')

    def setUp(self):
        '''
        Создаём клиенты.
        '''
        self.guest_client = Client()

        self.authorized_client = Client()
        self.authorized_client.force_login(UsersURLTests.user)

    def test_users_urls_url_exist_anonimus_user(self):
        '''
        Проверяем доступность URL для анонимного пользователя.
        '''
        verifiable_URLs = (
            '/auth/logout/',
            '/auth/signup/',
            '/auth/login/',
            '/auth/password_reset/',
            '/auth/password_reset/done/',
            '/auth/reset/done/',
        )
        for verifiable_URL in verifiable_URLs:
            with self.subTest(verifiable_URL=verifiable_URL):
                response = self.guest_client.get(verifiable_URL)
                self.assertEqual(
                    response.status_code, HTTPStatus.OK,
                    (
                        'Тест не пройден,'
                        f' {verifiable_URL} не доступен для анонимного юзера'
                    )
                )

    def test_users_urls_redirect_anonimus_user(self):
        '''
        Проверяем редиректы для анонимного пользователя.
        '''
        redirect_URLs = {
            '/auth/password_change/':
            '/auth/login/?next=/auth/password_change/',
            '/auth/password_change/done/':
            '/auth/login/?next=/auth/password_change/done/',
        }
        for url, redirect_url in redirect_URLs.items():
            with self.subTest(url=url, redirect_url=redirect_url):
                response = self.guest_client.get(url)
                self.assertRedirects(response, redirect_url)

    def test_users_urls_url_exist_authorized_user(self):
        '''
        Проверяем доступность URL для пользователя.
        '''
        verifiable_URLs = (
            '/auth/logout/',
        )
        for url in verifiable_URLs:
            with self.subTest(url=url):
                response = self.authorized_client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)
