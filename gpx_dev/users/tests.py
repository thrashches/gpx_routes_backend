from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.test import TestCase
from django.utils import timezone

from users.models import Follow

User = get_user_model()


class UserModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="test@email.com", nickname="testuser", password="testpass"
        )

        self.superuser = User.objects.create_superuser(
            email="super@email.com", nickname="superuser", password="superpass"
        )

    def test_user_creation(self):
        self.assertEqual(self.user.email, "test@email.com")
        self.assertEqual(self.user.nickname, "testuser")
        self.assertTrue(self.superuser.is_active)
        self.assertFalse(self.user.is_staff)
        self.assertFalse(self.user.is_superuser)

    def test_superuser_creation(self):
        self.assertEqual(self.superuser.email, "super@email.com")
        self.assertEqual(self.superuser.nickname, "superuser")
        self.assertTrue(self.superuser.is_active)
        self.assertTrue(self.superuser.is_staff)
        self.assertTrue(self.superuser.is_superuser)

    def test_user_str(self):
        self.assertEqual(str(self.user), self.user.email)

    def test_unique_users_nickname(self):
        with self.assertRaises(IntegrityError):
            User.objects.create_user(
                email="email@email.com",
                nickname=self.user.nickname,
                password="newtestpass",
            )

    def test_unique_users_email(self):
        with self.assertRaises(IntegrityError):
            User.objects.create_user(
                email=self.superuser.email,
                nickname="newnickname",
                password="newtestpass",
            )


# -------------------------------------------------------#


class FollowTestCase(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            nickname="user1", password="pass", email="email1@email.com"
        )
        self.user2 = User.objects.create_user(
            nickname="user2", password="pass", email="email2@email.com"
        )

    def test_create_follow(self):
        follow = Follow.objects.create(follower=self.user1, followee=self.user2)
        self.assertEqual(follow.follower, self.user1)
        self.assertEqual(follow.followee, self.user2)
        self.assertIsNotNone(follow.created)
        self.assertEqual(follow.status, Follow.Status.ACTIVE)

    def test_unique_follow(self):
        Follow.objects.create(follower=self.user1, followee=self.user2)

        with self.assertRaises(IntegrityError):
            Follow.objects.create(follower=self.user1, followee=self.user2)

    def test_follow_manager_active(self):
        Follow.objects.create(
            follower=self.user1, followee=self.user2, status=Follow.Status.ACTIVE
        )
        self.assertEqual(Follow.objects.active().count(), 1)

    def test_follow_manager_canceled(self):
        Follow.objects.create(
            follower=self.user1, followee=self.user2, status=Follow.Status.CANCELED
        )
        self.assertEqual(Follow.objects.canceled().count(), 1)

    def test_cancel_follow(self):
        follow = Follow.objects.create(follower=self.user1, followee=self.user2)

        self.assertEqual(follow.status, Follow.Status.ACTIVE)

        follow.status = Follow.Status.CANCELED
        follow.save()

        self.assertEqual(
            Follow.objects.get(id=follow.id).status, Follow.Status.CANCELED
        )
