from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from django import forms

User = get_user_model()


class UsersPagesNameTest(TestCase):
    '''
    Класс PostsPagesNameTest.
    Тестируем страницы и представления приложения posts.
    '''
    @classmethod
    def setUpClass(cls):
        '''
        Создаём 1 экземпляр модели Users.
        '''
        super().setUpClass()
        cls.user = User.objects.create_user(username='usertest')

    def setUp(self):
        '''
        Создаём гостевого и авторизированного клиента.
        '''
        self.guest_client = Client()

        self.authorized_client = Client()
        self.authorized_client.force_login(UsersPagesNameTest.user)

    def test_users_views_pages_use_correct_template(self):
        '''
        Проверяем, что views используют верные шаблоны.
        '''
        posts_templates = {
            reverse('users:signup'): 'users/signup.html',
            reverse('users:logout'): 'users/logged_out.html',
            reverse('users:login'): 'users/login.html',
            reverse('users:password_reset'): 'users/password_reset_form.html',
            reverse(
                'users:password_reset_done'
            ): 'users/password_reset_done.html',
        }
        for reverse_name, template in posts_templates.items():
            with self.subTest(template=template):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def test_users_views_user_create_correct_context(self):
        '''
        Шаблон сформирован с правильным контекстом.
        '''
        response = self.guest_client.get(
            reverse('users:signup')
        )
        form_fields = {
            'first_name': forms.fields.CharField,
            'last_name': forms.fields.CharField,
            'username': forms.fields.CharField,
            'email': forms.fields.EmailField,
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context.get('form').fields.get(value)
                self.assertIsInstance(form_field, expected)
