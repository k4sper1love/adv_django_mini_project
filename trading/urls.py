from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OrderViewSet, TransactionViewSet
from django.urls import path
from .views import execute_trade

router = DefaultRouter()
router.register(r"orders", OrderViewSet)
router.register(r"transactions", TransactionViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("execute_trade/", execute_trade, name="execute_trade"),
]
