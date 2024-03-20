from django.test import TestCase

from users.factories import UserExtendedFactory


class UsersTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = UserExtendedFactory()

    def test_user_telegram_id_unique(self):
        """ Проверка что telegram_id уникально """
        with self.assertRaises(Exception):
            [UserExtendedFactory(telegram_id='the_same_id') for _ in range(2)]
