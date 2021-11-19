import shutil
import tempfile
import time

from django.contrib.auth import get_user_model
from django.test import Client, TestCase, override_settings
from django.urls import reverse
from django.core.cache import cache
from django.core.files.uploadedfile import SimpleUploadedFile
from django.conf import settings

from posts.models import Post, Group, Comment

from yatube.settings import COUNT_OF_PAGE_POST, TIME_CACHED

User = get_user_model()

# Временная папка для медиа файлов
TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)


class PostsPagesNameTest(TestCase):
    '''
    Класс PostsPagesNameTest.
    Тестируем страницы и представления приложения posts.
    '''
    @classmethod
    def setUpClass(cls):
        '''
        Создаём 1 экземпляр модели Post.
        '''
        super().setUpClass()
        cls.user = User.objects.create_user(username='usertest')
        cls.group = Group.objects.create(
            title='Тестовая группа 1',
            slug='slug-g1',
            description='Тестовое описание группы 1',
        )
        cls.post: Post = Post.objects.create(
            author=cls.user,
            text='Тестовый пост 1',
            group=cls.group
        )

    def setUp(self):
        '''
        Создаём гостевого и авторизированного клиента.
        '''
        cache.clear()
        self.guest_client = Client()

        self.authorized_client = Client()
        self.authorized_client.force_login(PostsPagesNameTest.user)

    def test_posts_views_pages_use_correct_template(self):
        '''
        Проверяем, что views используют верные шаблоны.
        '''
        posts_templates = {
            reverse('posts:index'): 'posts/index.html',
            reverse(
                'posts:group_list',
                kwargs={'slug': 'slug-g1'}
            ): 'posts/group_list.html',
            reverse(
                'posts:profile',
                kwargs={'username': 'usertest'}
            ): 'posts/profile.html',
            reverse(
                'posts:post_detail',
                kwargs={'post_id': 1}
            ): 'posts/post_details.html',
            reverse(
                'posts:post_create'
            ): 'posts/create_post.html',
            reverse(
                'posts:post_edit',
                kwargs={'post_id': 1}
            ): 'posts/create_post.html'
        }
        for reverse_name, template in posts_templates.items():
            with self.subTest(template=template):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)


class PostsPaginatorViewsTest(TestCase):
    '''
    Класс PostsPaginatorViewsTest.
    Тестируем работу пагинатора в приложении posts.
    '''
    @classmethod
    def setUpClass(cls):
        '''
        Создаём экземплярs модели Post перед каждым тестом.
        '''
        super().setUpClass()
        cls.user = User.objects.create_user(username='usertest')
        cls.group = Group.objects.create(
            title='Тестовая группа 1',
            slug='slug-g1',
            description='Тестовое описание группы 1',
        )
        cls.count_posts = int(COUNT_OF_PAGE_POST * 1.5)
        cls.posts = []
        for i in range(cls.count_posts):
            cls.posts.append(
                Post.objects.create(
                    author=cls.user,
                    text=f'Тестовый пост {i}',
                    group=cls.group
                )
            )

    def setUp(self):
        '''
        Создаём гостевого и авторизированного клиента.
        '''
        cache.clear()
        self.guest_client = Client()

        self.authorized_client = Client()
        self.authorized_client.force_login(PostsPaginatorViewsTest.user)

        self.pages = (
            reverse('posts:index'),
            reverse('posts:group_list', kwargs={'slug': 'slug-g1'}),
            reverse('posts:profile', kwargs={'username': 'usertest'}),
        )

    def test_posts_views_paginator_first_page(self):
        '''
        Тестируем первую страницу при использовании пагинатора.
        '''
        for page in self.pages:
            with self.subTest(page=page):
                response = self.guest_client.get(page)
                self.assertEqual(
                    len(response.context['page_obj']),
                    COUNT_OF_PAGE_POST
                )

    def test_posts_views_paginator_second_page(self):
        '''
        Тестируем вторую страницу при использовании пагинатора.
        '''
        for page in self.pages:
            with self.subTest(page=page):
                response = self.guest_client.get(page + '?page=2')
                self.assertEqual(
                    len(response.context['page_obj']),
                    (PostsPaginatorViewsTest.count_posts - COUNT_OF_PAGE_POST)
                )


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class PostsContextTest(TestCase):
    '''
    Класс PostsContextTest.
    Тестируем контекст на страницах.
    '''
    @classmethod
    def setUpClass(cls):
        '''
        Создаём экземпляр модели Post.
        '''
        super().setUpClass()
        cls.user = User.objects.create_user(username='usertest')
        cls.user2 = User.objects.create_user(username='usertest2')
        cls.small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x02\x00'
            b'\x01\x00\x80\x00\x00\x00\x00\x00'
            b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
            b'\x00\x00\x00\x2C\x00\x00\x00\x00'
            b'\x02\x00\x01\x00\x00\x02\x02\x0C'
            b'\x0A\x00\x3B'
        )
        cls.uploaded = SimpleUploadedFile(
            name='small.gif',
            content=cls.small_gif,
            content_type='image/gif'
        )
        cls.group = Group.objects.create(
            title='Тестовая группа 1',
            slug='slug-g1',
            description='Тестовое описание группы 1',
        )
        cls.group2 = Group.objects.create(
            title='Тестовая группа 2',
            slug='slug-g2',
            description='Тестовое описание группы 2',
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовый пост 1',
            group=cls.group,
            image=cls.uploaded
        )
        cls.comment: Comment = Comment.objects.create(
            author=cls.user,
            post=cls.post,
            text='Тестовый комментарий'
        )

    def setUp(self):
        '''
        Создаём гостевого и авторизированного клиента.
        '''
        cache.clear()
        self.guest_client = Client()

        self.authorized_client = Client()
        self.authorized_client.force_login(PostsContextTest.user)
        self.other_authorized_client = Client()
        self.other_authorized_client.force_login(PostsContextTest.user2)

    @classmethod
    def tearDownClass(cls):
        '''
        Удаляем лишнее по завершении тестов.
        '''
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def check_post(self, post, text, author, group=None, image=None):
        '''
        Проверяем что экземпляр Post содержит ожидаемые значения
        '''
        self.assertEqual(
            post.text, text,
            'Тест не пройден, текст поста не совпадает с ожидаемым')
        self.assertEqual(
            post.group, group,
            'Тест не пройден, группа поста не совпадает с ожидаемой')
        self.assertEqual(
            post.author, author,
            'Тест не пройден, автор поста не совпадает с ожидаемым')
        self.assertEqual(
            post.image, image,
            'Тест не пройден, картинка поста не совпадает с ожидаемым')

    def check_comment(self, comment: Comment, post, author, text):
        '''
        Проверяем, что экземпляр коммента содержит ожидаемые значения.
        '''
        self.assertEqual(
            comment.post, post,
            'Тест не пройден, комментарий не к тому посту')
        self.assertEqual(
            comment.author, author,
            'Тест не пройден, комментарий не тому автору присваивается')
        self.assertEqual(
            comment.text, text,
            'Тест не пройден, текст комментарий не совпадает с ожидаемым')

    def test_posts_views_post_detail_correct_context(self):
        '''
        Проверяем контекст отдельного поста.
        '''
        response = self.guest_client.get(
            reverse(
                'posts:post_detail',
                kwargs={'post_id': 1}
            )
        )
        post = response.context['post']
        expected_post = PostsContextTest.post

        self.check_post(
            post,
            expected_post.text,
            expected_post.author,
            expected_post.group,
            expected_post.image
        )
        comment = response.context['comments'][0]
        expected_comment = PostsContextTest.comment
        self.check_comment(
            comment,
            expected_comment.post,
            expected_comment.author,
            expected_comment.text
        )

    def test_posts_views_page_show_correct_context(self):
        '''
        В шаблоны передан верный контекст.
        '''
        pages = {
            reverse('posts:index'):
                PostsContextTest.post,
            reverse('posts:group_list', kwargs={'slug': 'slug-g1'}):
                PostsContextTest.post,
            reverse('posts:profile', kwargs={'username': 'usertest'}):
                PostsContextTest.post,
        }
        for page, expected_post in pages.items():
            with self.subTest(page=page):
                response = (self.guest_client.get(page))
                post = response.context['page_obj'][0]
                self.check_post(
                    post,
                    expected_post.text,
                    expected_post.author,
                    expected_post.group,
                    expected_post.image)

    def test_posts_views_page_index_cached(self):
        '''
        Тестируем кеширование.
        '''
        response = self.authorized_client.get(reverse('posts:index'))
        count_posts_in_response = len(response.context['page_obj'])
        new_post = Post.objects.create(
            author=PostsContextTest.user,
            text='Тестовый пост 2'
        )
        new_post.save()
        response = self.authorized_client.get(reverse('posts:index'))
        # print(len(response.context['page_obj']))
        self.assertIsNone(
            response.context,
            (
                'Тест не пройден, новый контекст передался после'
                'создания нового поста, хотя должен был кешироватсья'
            )
        )
        time.sleep(TIME_CACHED / 2)
        response = self.authorized_client.get(reverse('posts:index'))
        self.assertIsNone(
            response.context,
            (
                'Тест не пройден, новый контекст передался после создания'
                'нового поста, хотя должен был кешироватсья'
            )
        )
        time.sleep(TIME_CACHED / 2)
        response = self.authorized_client.get(reverse('posts:index'))
        self.assertEqual(
            len(response.context['page_obj']), count_posts_in_response + 1,
            'Тест не пройден, должен был уже новый пост отобразиться')
