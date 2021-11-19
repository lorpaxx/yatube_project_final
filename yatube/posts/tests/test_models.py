from django.contrib.auth import get_user_model
from django.test import TestCase

from ..models import Comment, Group, Post, Follow

User = get_user_model()


class PostModelsTest(TestCase):
    '''
    Тестируем модель Post.
    '''
    @classmethod
    def setUpClass(cls):
        '''
        Создаём 1 экземпляр модели Post перед каждым тестом.
        '''
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.group = Group.objects.create(
            title='Тестовая группа для игры в WarCraft III',
            slug='Тестовый слаг',
            description='Тестовое описание',
        )
        cls.post: Post = Post.objects.create(
            author=cls.user,
            text='Тестовая группа для игры в WarCraft III',
        )

    def test_posts_models_Post_have_correct_object_names(self):
        """
        Проверяем, что у модели Post корректно работает __str__.
        """
        post: Post = PostModelsTest.post
        text = str(post)
        self.assertEqual(
            text,
            'Тестовая группа',
            'Тест не пройден, __str__ Post выводит не 15 символов')

    def test_posts_models_Post_have_correct_verbose_name(self):
        '''
        Пробежимся по полям модели Post и проверим verbose_name.
        '''
        field_verboses = {
            'text': 'Текст поста',
            'pub_date': 'Дата и время публикации поста',
            'author': 'Автор поста',
            'group': 'Группа',
        }
        post: Post = PostModelsTest.post
        for field, expected_value in field_verboses.items():
            with self.subTest(field=field):
                self.assertEqual(
                    post._meta.get_field(field).verbose_name,
                    expected_value,
                    'Тест не пройден'
                )

    def test_posts_models_Post_have_correct_help_text(self):
        '''
        Пробежимся по полям модели Post и проверим help_text.
        '''
        field_help_text = {
            'text': 'Текст нового поста',
            'pub_date': 'Дата и время публикации поста',
            'author': 'Автор поста',
            'group': 'Группа, к которой будет относиться пост',
        }
        post: Post = PostModelsTest.post
        for field, expected_value in field_help_text.items():
            with self.subTest(field=field):
                self.assertEqual(
                    post._meta.get_field(field).help_text,
                    expected_value
                )


class GroupModelsTest(TestCase):
    '''
    Тестируем модель Group.
    '''
    @classmethod
    def setUpClass(cls):
        '''
        Создаём 1 экземпляр модели Group перед каждым тестом.
        '''
        super().setUpClass()
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='Тестовый слаг',
            description='Тестовое описание',
        )

    def test_posts_models_Group_have_correct_object_names(self):
        """
        Проверяем, что у модели Group корректно работает __str__.
        """
        group: Group = GroupModelsTest.group
        title = group.title
        self.assertEqual(
            title,
            'Тестовая группа',
            'Тест не пройден, __str__ Group выводит не Group.title')

    def test_posts_models_Group_have_correct_verbose_name(self):
        '''
        Пробежимся по полям модели Group и проверим verbose_name.
        '''
        field_verboses = {
            'title': 'Группа',
            'slug': 'Tag группы',
            'description': 'Описание группы'
        }
        group: Group = GroupModelsTest.group
        for field, expected_value in field_verboses.items():
            with self.subTest(field=field):
                self.assertEqual(
                    group._meta.get_field(field).verbose_name,
                    expected_value,
                    'Тест не пройден'
                )

    def test_posts_models_Group_have_correct_help_text(self):
        '''Пробежимся по полям модели Post и проверим help_text.'''
        field_help_text = {
            'title': 'Группа, к которой будет относиться пост',
            'slug': 'Tag группы',
            'description': 'Краткое описание группы'
        }
        group: Group = GroupModelsTest.group
        for field, expected_value in field_help_text.items():
            with self.subTest(field=field):
                self.assertEqual(
                    group._meta.get_field(field).help_text,
                    expected_value,
                    'Тест не пройден'
                )


class CommentModelsTest(TestCase):
    '''
    Тестируем модель Models.
    '''
    @classmethod
    def setUpClass(cls):
        '''
        Создаём 1 экземпляр модели Comment перед каждым тестом.
        '''
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.comment_user = User.objects.create_user(username='comment_auth')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='slug_g',
            description='Тестовое описание группы',
        )
        cls.post = Post.objects.create(
            text='Тестовый пост',
            author=cls.user,
            group=cls.group,
        )
        cls.comment = Comment.objects.create(
            post=cls.post,
            author=cls.comment_user,
            text='Тестовый комментарий'
        )

    def test_posts_models_Comment_have_correct_object_names(self):
        """
        Проверяем, что у модели Comment корректно работает __str__.
        """
        comment: Comment = CommentModelsTest.comment
        text = str(comment)
        self.assertEqual(
            text,
            'Тестовый коммен',
            'Тест не пройден, __str__ Comment выводит не Comment.text')

    def test_posts_models_Comment_have_correct_verbose_name(self):
        '''
        Пробежимся по полям модели Comment и проверим verbose_name.
        '''
        field_verboses = {
            'post': 'Комментарий',
            'author': 'Автор комментария',
            'text': 'Текст комментария'
        }
        comment: Comment = CommentModelsTest.comment
        for field, expected_value in field_verboses.items():
            with self.subTest(field=field):
                self.assertEqual(
                    comment._meta.get_field(field).verbose_name,
                    expected_value,
                    'Тест не пройден'
                )

    def test_posts_models_Comment_have_correct_help_text(self):
        '''Пробежимся по полям модели Comment и проверим help_text.'''
        field_help_text = {
            'post': 'Комментарий к посту',
            'author': 'Автор комментария',
            'text': 'Текст комментария'
        }
        comment: Comment = CommentModelsTest.comment
        for field, expected_value in field_help_text.items():
            with self.subTest(field=field):
                self.assertEqual(
                    comment._meta.get_field(field).help_text,
                    expected_value,
                    'Тест не пройден'
                )


class FollowModelTest(TestCase):
    '''
    Тестируем модель Follow.
    '''
    @classmethod
    def setUpClass(cls):
        '''
        Создаём 1 экземпляр модели Follow.
        '''
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.follow_user = User.objects.create_user(username='follow_auth')
        cls.follow = Follow.objects.create(
            user=cls.user,
            author=cls.follow_user,
        )

    def test_posts_models_Follow_have_correct_object_names(self):
        """
        Проверяем, что у модели Comment корректно работает __str__.
        """
        follow: Follow = FollowModelTest.follow
        text = str(follow)
        self.assertEqual(
            text,
            'auth: follow_auth',
            'Тест не пройден, __str__ Follow выводит неожидаемое')

    def test_posts_models_Follow_have_correct_verbose_name(self):
        '''
        Пробежимся по полям модели Follow и проверим verbose_name.
        '''
        field_verboses = {
            'user': 'Подписчик',
            'author': 'Автор',
        }
        follow: Follow = FollowModelTest.follow
        for field, expected_value in field_verboses.items():
            with self.subTest(field=field):
                self.assertEqual(
                    follow._meta.get_field(field).verbose_name,
                    expected_value,
                    'Тест не пройден'
                )

    def test_posts_models_Follow_have_correct_help_text(self):
        '''Пробежимся по полям модели Comment и проверим help_text.'''
        field_help_text = {
            'user': 'Подписчик',
            'author': 'Автор'
        }
        follow: Follow = FollowModelTest.follow
        for field, expected_value in field_help_text.items():
            with self.subTest(field=field):
                self.assertEqual(
                    follow._meta.get_field(field).help_text,
                    expected_value,
                    'Тест не пройден'
                )
