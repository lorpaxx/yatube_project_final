from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse


User = get_user_model()


class CreationFormTest(TestCase):
    '''
    Класс CreationFormTest.
    '''
    def setUp(self):
        '''
        Создаём гоствой клиент.
        '''
        self.guest_client = Client()

    def test_users_forms_create_new_users(self):
        '''
        Проверяем, что новый пользователь создался.
        '''
        user_count = User.objects.count()
        form_data = {
            'first_name': 'Ар',
            'last_name': 'Кад',
            'username': 'arkad',
            'email': 'kadar@yandex.ru',
            'password1': '123456_qwerty',
            'password2': '123456_qwerty'
        }
        response = self.guest_client.post(
            reverse('users:signup'),
            data=form_data,
            follow=True
        )
        self.assertRedirects(
            response,
            reverse('posts:index')
        )
        self.assertEqual(
            User.objects.count(),
            user_count + 1,
            'пользователь не появился'
        )
        self.assertTrue(
            User.objects.filter(
                first_name='Ар',
                last_name='Кад',
                username='arkad',
                email='kadar@yandex.ru',
            ).exists(), 'А нет такого пользователя'
        )
