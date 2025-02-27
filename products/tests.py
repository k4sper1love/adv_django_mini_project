from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models import Product, Category

User = get_user_model()

class ProductAPITestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", email="user@test.com", password="testpass")
        self.client.force_authenticate(user=self.user)

        self.category = Category.objects.create(name="Electronics")
        self.product = Product.objects.create(name="Laptop", category=self.category, price=1000)

        self.category_list_url = reverse("category-list")
        self.product_list_url = reverse("product-list")

    def test_get_categories(self):
        response = self.client.get(self.category_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_category(self):
        data = {"name": "Books"}
        response = self.client.post(self.category_list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_products(self):
        response = self.client.get(self.product_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_product(self):
        data = {"name": "Smartphone", "category": self.category.id, "price": 500}
        response = self.client.post(self.product_list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
