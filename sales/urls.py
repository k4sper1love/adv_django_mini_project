from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SalesOrderViewSet, InvoiceViewSet

router = DefaultRouter()
router.register(r"sales-orders", SalesOrderViewSet, basename="salesorder")
router.register(r"invoices", InvoiceViewSet, basename="invoice")

urlpatterns = [
    path("", include(router.urls)),
]
