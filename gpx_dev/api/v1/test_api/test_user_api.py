from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from users.models import User, Follow


class UserViewSetTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="test@email.com", nickname="user1", password="testpass"
        )

        self.user2 = User.objects.create_user(
            email="test2@email.com", nickname="user2", password="superpass"
        )

    def test_list_users(self):
        url = reverse("user-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_get_me(self):
        url = reverse("user-me")
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["nickname"], self.user.nickname)

    def test_update_me(self):
        url = reverse("user-me")
        new_nickname = "new_nickname"
        data = {"nickname": new_nickname}
        self.client.force_authenticate(user=self.user)
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.nickname, new_nickname)
        self.assertEqual(url, "/api/v1/users/me/")

    def test_create_user(self):
        """
        С простым паролем и без подтверждения не работает
        """

        url = reverse("user-list")
        data = {
            "email": "newuser@example.com",
            "nickname": "newuser",
            "password": "newpassword123",
            "password_confirm": "newpassword123",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(email=data["email"]).exists())
        self.assertEqual(url, "/api/v1/users/")

    def test_search_users(self):
        url = reverse("user-list")
        search_param = "user2"
        response = self.client.get(url, {"search": search_param})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["nickname"], self.user2.nickname)
        self.assertTrue("search" in response.request.get("QUERY_STRING"))
        self.assertEqual(response.request.get("QUERY_STRING"), f"search={search_param}")

    def test_search_two_users(self):
        url = reverse("user-list")
        search_param = "user"  # У обоих пользователей в нике есть user
        response = self.client.get(url, {"search": search_param})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_subscribe(self):
        url = reverse("user-subscribe", kwargs={"nickname": self.user.nickname})

        # try follow to self
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["error"], "You can't subscribe yourself")

        # follow to other
        url2 = reverse("user-subscribe", kwargs={"nickname": self.user2.nickname})
        response = self.client.post(url2)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # try second follow
        response = self.client.post(url2)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["error"], "Already following")

    def test_unsubscribe(self):
        Follow.objects.create(follower=self.user, followee=self.user2)

        url = reverse("user-unsubscribe", kwargs={"nickname": self.user.nickname})

        # try to unsubscribe self
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["error"], "You can't unsubscribe yourself")

        # success unsubscribe
        url = reverse("user-unsubscribe", kwargs={"nickname": self.user2.nickname})

        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(
            Follow.objects.filter(follower=self.user, followee=self.user2).exists()
        )

        # try second unsub when already unsub
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["error"], "You are not following this user")
