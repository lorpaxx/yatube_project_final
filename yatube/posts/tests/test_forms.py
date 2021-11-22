import shutil
import tempfile

from posts.models import Post, Group, User, Comment

from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase, override_settings
from django.urls import reverse
from django import forms


TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class PostFormTests(TestCase):
    '''
    Класс PostFormTests.
    Тестируем работу формы PostForm.
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
            text='Тестовый 1',
            group=cls.group
        )
        cls.group2 = Group.objects.create(
            title='Тестовая группа 2',
            slug='slug-g2',
            description='Тестовое описание группы 2',
        )

    @classmethod
    def tearDownClass(cls):
        '''
        Удаляем лишнее по завершении тестов.
        '''
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def setUp(self):
        '''
        Создаём авторизированного клиента.
        '''
        self.authorized_client = Client()
        self.authorized_client.force_login(PostFormTests.user)

    def test_posts_forms_post_create_correct_context(self):
        '''
        Шаблон сформирован с правильным контекстом.
        '''
        response = self.authorized_client.get(
            reverse('posts:post_create')
        )
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField,
            'image': forms.fields.ImageField
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context.get('form').fields.get(value)
                self.assertIsInstance(
                    form_field, expected,
                    f'Тест не пройден, тип поля {value} не совпадает'
                )

    def test_posts_forms_post_edit_correct_context(self):
        '''
        Шаблон сформирован с правильным контекстом.
        '''
        response = self.authorized_client.get(
            reverse('posts:post_edit', kwargs={'post_id': 1})
        )
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField,
            'image': forms.fields.ImageField
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context.get('form').fields.get(value)
                self.assertIsInstance(
                    form_field, expected,
                    f'Тест не пройден, тип поля {value} не совпадает'
                )

    def test_posts_forms_create_post(self):
        '''
        Проверяем, что с помощью формы пост сохраняется в БД.
        '''
        post_count = Post.objects.count()
        post_group = Post.objects.filter(
            group=PostFormTests.group
        ).count()
        post_other_group = Post.objects.filter(
            group=PostFormTests.group2
        ).count()
        post_user = Post.objects.filter(
            author=PostFormTests.user
        ).count()
        small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x02\x00'
            b'\x01\x00\x80\x00\x00\x00\x00\x00'
            b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
            b'\x00\x00\x00\x2C\x00\x00\x00\x00'
            b'\x02\x00\x01\x00\x00\x02\x02\x0C'
            b'\x0A\x00\x3B'
        )
        uploaded = SimpleUploadedFile(
            name='small.gif',
            content=small_gif,
            content_type='image/gif'
        )
        form_data = {
            'text': 'Тестовый 2',
            'group': PostFormTests.group.id,
            'image': uploaded
        }
        response = self.authorized_client.post(
            reverse('posts:post_create'),
            data=form_data,
            follow=True
        )
        self.assertRedirects(
            response,
            reverse('posts:profile', kwargs={'username': 'usertest'})
        )
        self.assertEqual(
            Post.objects.count(), post_count + 1,
            'Тест не пройден, новый пост не сохранился в БД')
        self.assertTrue(
            Post.objects.filter(
                text='Тестовый 2',
                group=PostFormTests.group,
                image='posts/small.gif'
            ).exists(),
            'Тест не пройден, данные из формы не перенеслись в базу'
        )
        self.assertEqual(
            Post.objects.filter(
                group=PostFormTests.group
            ).count(), post_group + 1,
            'Тест не пройден, у нового поста не проставилась группа'
        )
        self.assertEqual(
            Post.objects.filter(
                author=PostFormTests.user
            ).count(), post_user + 1,
            'Тест не пройден, у нового поста не тот автор'
        )
        self.assertEqual(
            Post.objects.filter(
                group=PostFormTests.group2
            ).count(), post_other_group,
            'Тест не пройден, у нового поста проставилась другая группа'
        )

    def test_posts_forms_edit_post(self):
        '''
        Проверяем, что что пост изменился.
        '''
        post_count = Post.objects.count()
        little_gif = (
            b'\x47\x49\x46\x38\x39\x61\x02\x00'
            b'\x01\x00\x80\x00\x00\x00\x00\x00'
            b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
            b'\x00\x00\x00\x2C\x00\x00\x00\x00'
            b'\x02\x00\x01\x00\x00\x02\x02\x0C'
            b'\x0A\x00\x3B'
        )
        uploaded = SimpleUploadedFile(
            name='little.gif',
            content=little_gif,
            content_type='image/gif'
        )
        form_data = {
            'text': 'Тестовый 1 (редактирован)',
            'group': PostFormTests.group2.id,
            'image': uploaded
        }
        response = self.authorized_client.post(
            reverse('posts:post_edit', kwargs={'post_id': 1}),
            data=form_data,
            follow=True
        )
        self.assertRedirects(
            response,
            reverse('posts:post_detail', kwargs={'post_id': 1})
        )
        self.assertEqual(Post.objects.count(), post_count)
        self.assertTrue(
            Post.objects.filter(
                text='Тестовый 1 (редактирован)',
                group=PostFormTests.group2,
                image='posts/little.gif'
            ).exists()
        )


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class CommentFormTests(TestCase):
    '''
    Класс CommentFormTests.
    Тестируем работу формы CommentForm.
    '''
    @classmethod
    def setUpClass(cls):
        '''
        Создаём 1 экземпляр модели Post и Comments.
        '''
        super().setUpClass()
        cls.user = User.objects.create_user(username='usertest')
        cls.user2 = User.objects.create_user(username='usertest2')
        cls.group = Group.objects.create(
            title='Тестовая группа 1',
            slug='slug-g1',
            description='Тестовое описание группы 1',
        )
        cls.post: Post = Post.objects.create(
            author=cls.user,
            text='Тестовый пост',
            group=cls.group
        )
        cls.comment: Comment = Comment.objects.create(
            post=cls.post,
            author=cls.user2,
            text='Тестовый комментарий'
        )

    @classmethod
    def tearDownClass(cls):
        '''
        Удаляем лишнее по завершении тестов.
        '''
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def setUp(self):
        '''
        Создаём авторизированного клиента.
        '''
        self.authorized_client = Client()
        self.authorized_client.force_login(CommentFormTests.user)
        self.authorized_client2 = Client()
        self.authorized_client2.force_login(CommentFormTests.user2)

    def test_posts_forms_comment_create_correct_context(self):
        '''
        Шаблон сформирован с правильным контекстом.
        '''
        response = self.authorized_client.get(
            reverse(
                'posts:post_detail',
                kwargs={'post_id': CommentFormTests.post.id})
        )
        form_fields = {
            'text': forms.fields.CharField,
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context.get('form').fields.get(value)
                self.assertIsInstance(
                    form_field, expected,
                    f'Тест не пройден, тип поля {value} не совпадает'
                )

    def test_posts_forms_create_comment(self):
        '''
        Проверяем, что с помощью формы комментарий сохраняется в БД.
        '''
        comment_count = Comment.objects.count()
        comment_user_count = Comment.objects.filter(
            author=CommentFormTests.user).count()
        comment_user2_count = Comment.objects.filter(
            author=CommentFormTests.user2).count()
        comment_post_count = Comment.objects.filter(
            post=CommentFormTests.post).count()

        form_data = {
            'text': 'Тестовый комментарий 2',
        }
        response = self.authorized_client2.post(
            reverse(
                'posts:add_comment',
                kwargs={'post_id': CommentFormTests.post.id}),
            data=form_data,
            follow=True
        )
        self.assertRedirects(
            response,
            reverse(
                'posts:post_detail',
                kwargs={'post_id': CommentFormTests.post.id}
            )
        )
        self.assertEqual(
            Comment.objects.count(), comment_count + 1,
            'Тест не пройден, новый комментарий не сохранился в БД')
        self.assertTrue(
            Comment.objects.filter(
                text='Тестовый комментарий 2',
                post=CommentFormTests.post,
                author=CommentFormTests.user2
            ).exists(),
            'Тест не пройден, данные из формы не перенеслись в базу'
        )
        self.assertEqual(
            Comment.objects.filter(
                post=CommentFormTests.post
            ).count(), comment_post_count + 1,
            'Тест не пройден, у поста не добавился комментарий'
        )
        self.assertEqual(
            Comment.objects.filter(
                author=CommentFormTests.user
            ).count(), comment_user_count,
            'Тест не пройден, у чужого пользователя добавился комментарий'
        )
        self.assertEqual(
            Comment.objects.filter(
                author=CommentFormTests.user2
            ).count(), comment_user2_count + 1,
            'Тест не пройден, у пользователя не добавился комментарий'
        )
