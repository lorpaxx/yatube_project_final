from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.test import TestCase, Client
from posts.models import Post, Group, Follow

from http import HTTPStatus


User = get_user_model()


class StaticURLTests(TestCase):
    '''
    Класс StaticURLTests.
    '''
    def setUp(self):
        '''
        Создаём клиента для каждого из тестов.
        '''
        self.guest_client = Client()

    def test_homepage(self):
        '''
        Тестируем наличие стартовой страницы.
        '''
        page = '/'
        response = self.guest_client.get(page)
        self.assertEqual(
            response.status_code, HTTPStatus.OK,
            f'Cтраница {page} не имеет status_code == 200'
        )

    def test_about_author(self):
        '''
        Тестируем наличие страницы "Об Авторе".
        '''
        page = '/about/author/'
        response = self.guest_client.get(page)
        self.assertEqual(
            response.status_code, HTTPStatus.OK,
            f'Cтраница {page} не имеет status_code == 200'
        )

    def test_about_tech(self):
        '''
        Тестируем наличие страницы "Технология".
        '''
        page = '/about/tech/'
        response = self.guest_client.get(page)
        self.assertEqual(
            response.status_code, 200,
            f'Cтраница {page} не имеет status_code == 200'
        )


class PostsURLTests(TestCase):
    '''
    Тестируем URL приложения posts.
    '''
    @classmethod
    def setUpClass(cls):
        '''
        Создаём записи в БД.
        '''
        super().setUpClass()
        cls.user = User.objects.create_user(username='NoName')
        cls.other_user = User.objects.create_user(username='Other_NoName')
        cls.follower_user = User.objects.create_user(
            username='Follower_NoName')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='test'
        )
        cls.post1 = Post.objects.create(
            text='Тестовый текст',
            author=cls.user,
            group=cls.group
        )
        cls.post2 = Post.objects.create(
            text='Тестовый текст 2',
            author=cls.other_user,
            group=cls.group
        )
        cls.follow1 = Follow.objects.create(
            user=cls.follower_user,
            author=cls.user
        )
        cls.follow2 = Follow.objects.create(
            user=cls.follower_user,
            author=cls.other_user
        )

    def setUp(self):
        cache.clear()
        self.guest_client = Client()

        self.authorized_client = Client()
        self.authorized_client.force_login(PostsURLTests.user)

        self.other_authorized_client = Client()
        self.other_authorized_client.force_login(PostsURLTests.other_user)

        self.follower_client = Client()
        self.follower_client.force_login(PostsURLTests.follower_user)

    def test_posts_urls_url_exist_anonimus_user(self):
        '''
        Проверяем доступность URL приложения posts для анонимного пользователя.
        '''
        verifiable_URLs = (
            '/',
            '/posts/1/',
            '/group/test/',
            '/profile/NoName/'
        )
        for verifiable_URL in verifiable_URLs:
            with self.subTest(verifiable_URL=verifiable_URL):
                response = self.guest_client.get(verifiable_URL)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_posts_urls_url_exist_authorized_user(self):
        '''
        Проверяем доступность URL для авторизированного пользователя.
        '''
        verifiable_URLs = (
            '/',
            '/posts/1/',
            '/posts/1/edit/',
            '/group/test/',
            '/profile/NoName/',
            '/create/',
        )
        for verifiable_URL in verifiable_URLs:
            with self.subTest(verifiable_URL=verifiable_URL):
                response = self.authorized_client.get(verifiable_URL)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_posts_urls_url_redirect_other_authorized_user(self):
        '''
        Проверяем перенаправление для пользователя, но не автора поста.
        '''
        redirect_URLs = {
            '/posts/1/edit/': '/posts/1/'
        }
        for url, redirect_URL in redirect_URLs.items():
            with self.subTest():
                response = self.other_authorized_client.get(url)
                self.assertRedirects(response, redirect_URL)

    def test_posts_urls_url_not_exist(self):
        '''
        Проверяем, что на некорректный URL получим 404.
        '''
        clients = (
            self.guest_client,
            self.authorized_client,
            self.other_authorized_client,
        )
        incorrect_URL = '/123/'
        for clt in clients:
            with self.subTest():
                response = clt.get(incorrect_URL)
                self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_posts_urls_template_correct_anonimus_user(self):
        '''
        Проверяем наименования используемых шаблонов для анонима.
        '''
        verifiable_URLs = {
            '/': 'posts/index.html',
            '/posts/1/': 'posts/post_details.html',
            '/group/test/': 'posts/group_list.html',
            '/profile/NoName/': 'posts/profile.html',

        }
        for url, template in verifiable_URLs.items():
            with self.subTest():
                response = self.guest_client.get(url)
                self.assertTemplateUsed(response, template)

    def test_posts_urls_template_correct_authorized_user(self):
        '''
        Проверяем наименования используемых шаблонов пользователя.
        '''
        verifiable_URLs = {
            '/': 'posts/index.html',
            '/posts/1/': 'posts/post_details.html',
            '/posts/1/edit/': 'posts/create_post.html',
            '/group/test/': 'posts/group_list.html',
            '/profile/NoName/': 'posts/profile.html',
            '/create/': 'posts/create_post.html',
            '/follow/': 'posts/follow.html'
        }
        for url, template in verifiable_URLs.items():
            with self.subTest(url=url, template=template):
                response = self.authorized_client.get(url)
                self.assertTemplateUsed(
                    response, template,
                    f'Тест не пройден, url {url} не содержит шаблон {template}'
                )

    def test_posts_urls_Follow_redirect_anonimus_user(self):
        '''
        Проверяем, что анонимы перенаправляются
        на страницу входа для Follow-страниц.
        '''
        verifiable_URLs = (
            '/follow/',
            '/profile/NoName/follow/',
            '/profile/NoName/unfollow/'
        )
        for verifiable_URL in verifiable_URLs:
            with self.subTest(verifiable_URL=verifiable_URL):
                response = self.guest_client.get(verifiable_URL)
                self.assertEqual(
                    response.status_code, 302,
                    f'Тест не пройден, не перенаправляется {verifiable_URL}')

    def test_posts_urls_Follow_exists_authorized_user(self):
        '''
        Проверяем, что пользователям доступны Follow-страницы.
        '''
        verifiable_URLs = (
            '/follow/',
        )
        for verifiable_URL in verifiable_URLs:
            with self.subTest(verifiable_URL=verifiable_URL):
                response = self.authorized_client.get(verifiable_URL)
                self.assertEqual(
                    response.status_code, 200,
                    f'Тест не пройден, не доступна {verifiable_URL}')
