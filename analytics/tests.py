from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models import TradeAnalytics

User = get_user_model()

class TradeAnalyticsAPITestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", email="user@test.com", password="testpass")
        self.client.force_authenticate(user=self.user)

        TradeAnalytics.objects.create(metric="Total Trades", value=100)
        TradeAnalytics.objects.create(metric="Total Profit", value=50000)

        self.analytics_url = reverse("trade-analytics")
        self.csv_url = reverse("download-csv-report")
        self.pdf_url = reverse("download-pdf-report")

    def test_get_trade_analytics(self):
        response = self.client.get(self.analytics_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_download_csv_report(self):
        response = self.client.get(self.csv_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response["Content-Type"], "text/csv")

    def test_download_pdf_report(self):
        response = self.client.get(self.pdf_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response["Content-Type"], "application/pdf")
