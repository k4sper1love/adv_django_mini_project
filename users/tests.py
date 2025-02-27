from django.test import TestCase

# Create your tests here.
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse

User = get_user_model()

class UserViewSetTestCase(APITestCase):

    def setUp(self):
        self.admin_user = User.objects.create_superuser(username="admin", email="admin@test.com", password="adminpass")
        self.regular_user = User.objects.create_user(username="user", email="user@test.com", password="userpass")

        self.client.force_authenticate(user=self.admin_user)
        self.user_list_url = reverse("user-list")

    def test_get_user_list_as_admin(self):
        response = self.client.get(self.user_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_user_list_as_non_admin(self):
        self.client.force_authenticate(user=self.regular_user)
        response = self.client.get(self.user_list_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_user(self):
        data = {
            "username": "newuser",
            "email": "newuser@test.com",
            "password": "newpass"
        }
        response = self.client.post(self.user_list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 3)

    def test_update_user(self):
        update_url = reverse("user-detail", args=[self.regular_user.id])
        data = {"username": "updateduser"}
        response = self.client.patch(update_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.regular_user.refresh_from_db()
        self.assertEqual(self.regular_user.username, "updateduser")

    def test_delete_user(self):
        delete_url = reverse("user-detail", args=[self.regular_user.id])
        response = self.client.delete(delete_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(User.objects.count(), 1)

    def test_non_admin_cannot_manage_users(self):
        self.client.force_authenticate(user=self.regular_user)

        data = {"username": "testuser"}
        create_response = self.client.post(self.user_list_url, data)
        self.assertEqual(create_response.status_code, status.HTTP_403_FORBIDDEN)

        update_url = reverse("user-detail", args=[self.regular_user.id])
        update_response = self.client.patch(update_url, {"username": "hacker"})
        self.assertEqual(update_response.status_code, status.HTTP_403_FORBIDDEN)

        delete_response = self.client.delete(update_url)
        self.assertEqual(delete_response.status_code, status.HTTP_403_FORBIDDEN)
