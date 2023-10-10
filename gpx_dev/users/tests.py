from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test import TestCase

from users.models import User


class UserModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@email.com',
            nickname='testuser',
            password='testpass'
        )

        self.superuser = User.objects.create_superuser(
            email='super@email.com',
            nickname='superuser',
            password='superpass'
        )

    def test_user_creation(self):
        self.assertEqual(self.user.email, 'test@email.com')
        self.assertEqual(self.user.nickname, 'testuser')
        self.assertTrue(self.superuser.is_active)
        self.assertFalse(self.user.is_staff)
        self.assertFalse(self.user.is_superuser)

    def test_superuser_creation(self):
        print(self.superuser.is_staff)
        self.assertEqual(self.superuser.email, 'super@email.com')
        self.assertEqual(self.superuser.nickname, 'superuser')
        self.assertTrue(self.superuser.is_active)
        self.assertTrue(self.superuser.is_staff)
        self.assertTrue(self.superuser.is_superuser)

    def test_user_str(self):
        self.assertEqual(str(self.user), self.user.email)

    def test_unique_users_nickname(self):
        with self.assertRaises(IntegrityError):
            User.objects.create_user(
                email='email@email.com',
                nickname=self.user.nickname,
                password='newtestpass'
            )

    def test_unique_users_email(self):
        with self.assertRaises(IntegrityError):
            User.objects.create_user(
                email=self.superuser.email,
                nickname='newnickname',
                password='newtestpass'
            )