from rest_framework import viewsets, permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import SalesOrder, Invoice
from .serializers import SalesOrderSerializer, InvoiceSerializer
from users.permissions import IsSalesRep

class SalesOrderViewSet(viewsets.ModelViewSet):
    queryset = SalesOrder.objects.all()
    serializer_class = SalesOrderSerializer
    permission_classes = [permissions.IsAuthenticated, IsSalesRep]

    @swagger_auto_schema(
        operation_description="Получить список заказов",
        responses={200: SalesOrderSerializer(many=True)}
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Создать новый заказ",
        request_body=SalesOrderSerializer,
        responses={201: SalesOrderSerializer()}
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


class InvoiceViewSet(viewsets.ModelViewSet):
    """
    API для управления счетами (Invoices).
    """
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer
    permission_classes = [permissions.IsAuthenticated, IsSalesRep]

    @swagger_auto_schema(
        operation_description="Получить список счетов",
        responses={200: InvoiceSerializer(many=True)}
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Создать новый счет",
        request_body=InvoiceSerializer,
        responses={201: InvoiceSerializer()}
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
