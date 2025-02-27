from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models import Notification

User = get_user_model()

class NotificationAPITestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", email="user@test.com", password="testpass")
        self.admin = User.objects.create_superuser(username="admin", email="admin@test.com", password="adminpass")
        self.client.force_authenticate(user=self.user)

        self.notification = Notification.objects.create(user=self.user, message="Test Notification")
        self.notification_list_url = reverse("notification-list")

    def test_get_notifications(self):
        response = self.client.get(self.notification_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_notification(self):
        self.client.force_authenticate(user=self.admin)
        data = {"user": self.user.id, "message": "New Notification"}
        response = self.client.post(self.notification_list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_cannot_create_notification(self):
        data = {"user": self.user.id, "message": "New Notification"}
        response = self.client.post(self.notification_list_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_mark_notification_as_read(self):
        url = reverse("notification-detail", args=[self.notification.id])
        response = self.client.patch(url, {"is_read": True})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.notification.refresh_from_db()
        self.assertTrue(self.notification.is_read)
