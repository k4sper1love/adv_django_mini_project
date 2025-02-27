from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models import SalesOrder, Invoice
from products.models import Product

User = get_user_model()

class SalesAPITestCase(APITestCase):

    def setUp(self):
        self.sales_rep = User.objects.create_user(username="sales", email="sales@test.com", password="salespass", is_staff=True)
        self.regular_user = User.objects.create_user(username="user", email="user@test.com", password="userpass")

        self.client.force_authenticate(user=self.sales_rep)

        self.product = Product.objects.create(name="Test Product", price=100)
        self.sales_order = SalesOrder.objects.create(user=self.sales_rep, product=self.product, quantity=2, total_price=200)
        self.invoice = Invoice.objects.create(sales_order=self.sales_order, invoice_number="INV-001")

        self.sales_order_list_url = reverse("salesorder-list")
        self.invoice_list_url = reverse("invoice-list")

    def test_get_sales_orders(self):
        response = self.client.get(self.sales_order_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_sales_order(self):
        data = {"user": self.sales_rep.id, "product": self.product.id, "quantity": 3, "total_price": 300}
        response = self.client.post(self.sales_order_list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_invoices(self):
        response = self.client.get(self.invoice_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_invoice(self):
        data = {"sales_order": self.sales_order.id, "invoice_number": "INV-002"}
        response = self.client.post(self.invoice_list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_non_sales_cannot_access(self):
        self.client.force_authenticate(user=self.regular_user)
        response = self.client.get(self.sales_order_list_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
