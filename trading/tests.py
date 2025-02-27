from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models import Order, Transaction

User = get_user_model()

class TradingAPITestCase(APITestCase):

    def setUp(self):
        self.trader = User.objects.create_user(username="trader", email="trader@test.com", password="traderpass", is_staff=True)
        self.regular_user = User.objects.create_user(username="user", email="user@test.com", password="userpass")

        self.client.force_authenticate(user=self.trader)

        self.order = Order.objects.create(trader=self.trader, asset="BTC", quantity=1, price=45000)
        self.transaction = Transaction.objects.create(order=self.order, status="completed")

        self.order_list_url = reverse("order-list")
        self.transaction_list_url = reverse("transaction-list")
        self.execute_trade_url = reverse("execute-trade")

    def test_get_orders_as_trader(self):
        response = self.client.get(self.order_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_transactions_as_trader(self):
        response = self.client.get(self.transaction_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_order(self):
        data = {"trader": self.trader.id, "asset": "ETH", "quantity": 2, "price": 3000}
        response = self.client.post(self.order_list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_transaction(self):
        data = {"order": self.order.id, "status": "pending"}
        response = self.client.post(self.transaction_list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_execute_trade(self):
        data = {"order_id": self.order.id}
        response = self.client.post(self.execute_trade_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_non_trader_cannot_access(self):
        self.client.force_authenticate(user=self.regular_user)
        response = self.client.get(self.order_list_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
