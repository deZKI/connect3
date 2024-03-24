from django.test import TestCase
from django.urls import reverse

from rest_framework import status

from users.factories import UserExtendedFactory
from users.models import UserExtended


class UserApiTests(TestCase):
    """ Тесты api пользователя"""

    @classmethod
    def setUpTestData(cls):
        # Создаем пользователя для тестирования
        cls.user = UserExtendedFactory(username="testuser")
        # Создаем пользователя-администратора
        cls.admin_user = UserExtended.objects.create_superuser('admin', 'admin@example.com', 'adminpass')

    def test_user_creation(self):
        """Проверка, что любой пользователь может создать пользователя"""
        url = reverse('users:register')
        data = {
            'username': 'newuser',
            'church': 'Test Church',
            'know_from': 'Internet',
            "password": "<PASSWORD>",
            "password2": "<PASSWORD>",
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['username'], 'newuser')
        self.assertNotIn('balance', response.data['username'])

        user = UserExtended.objects.filter(username=response.data['username']).first()
        self.assertEqual(user.username, 'newuser')

    def test_get_user_info(self):
        """Проверка, что любой пользователь может получить информацию о пользователе"""
        user = UserExtendedFactory.create()
        self.client.login(username='testuser', password='password')
        url = reverse('users:detail', kwargs={'pk': user.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], user.username)

    def test_delete_user(self):
        """Проверка, что нельзя удалить пользователя"""
        url = reverse('users:detail', kwargs={'pk': self.user.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_get_personal_data(self):
        """Проверка, что персональную информацию может получить только админ или сам пользователь"""
        self.client.login(username='admin', password='adminpass')
        url = reverse('users:detail', kwargs={'pk': self.user.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('balance', response.data)

        # Выход и вход под другим пользователем
        self.client.logout()
        self.client.login(username='testuser', password='password')
        response = self.client.get(url)
        # Убедимся, что персональная информация не доступна для других пользователей
        self.assertNotIn('balance', response.data)

