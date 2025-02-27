from rest_framework import viewsets, permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .tasks import process_trade
from .models import Order, Transaction
from .serializers import OrderSerializer, TransactionSerializer
from users.permissions import IsTrader


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated, IsTrader]

    @swagger_auto_schema(
        operation_description="Получить список ордеров",
        responses={200: OrderSerializer(many=True)}
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Получить данные ордера",
        responses={200: OrderSerializer()}
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Создать новый ордер",
        request_body=OrderSerializer,
        responses={201: OrderSerializer()}
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Обновить ордер",
        request_body=OrderSerializer,
        responses={200: OrderSerializer()}
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Удалить ордер",
        responses={204: 'Ордер удалён'}
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated, IsTrader]

    @swagger_auto_schema(
        operation_description="Получить список транзакций",
        responses={200: TransactionSerializer(many=True)}
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Получить данные транзакции",
        responses={200: TransactionSerializer()}
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Создать новую транзакцию",
        request_body=TransactionSerializer,
        responses={201: TransactionSerializer()}
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Обновить транзакцию",
        request_body=TransactionSerializer,
        responses={200: TransactionSerializer()}
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Удалить транзакцию",
        responses={204: 'Транзакция удалена'}
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


@swagger_auto_schema(
    method="post",
    operation_description="Запустить исполнение сделки (асинхронно через Celery)",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "order_id": openapi.Schema(type=openapi.TYPE_INTEGER, description="ID ордера")
        },
        required=["order_id"]
    ),
    responses={200: openapi.Response("Trade processing started!")}
)
@api_view(["POST"])
def execute_trade(request):
    order_id = request.data.get("order_id")
    if not order_id:
        return Response({"error": "order_id is required"}, status=400)

    process_trade.delay(order_id)
    return Response({"message": "Trade processing started!"}, status=200)
