from rest_framework import viewsets, permissions
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import Notification
from .serializers import NotificationSerializer
from users.permissions import IsUserOrAdmin

class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all().order_by("-created_at")
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated, IsUserOrAdmin]

    def get_queryset(self):
        """
        Ограничение списка уведомлений только для текущего пользователя.
        """
        return Notification.objects.filter(user=self.request.user)

    @swagger_auto_schema(
        operation_description="Получить список уведомлений пользователя",
        responses={200: NotificationSerializer(many=True)}
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Создать новое уведомление",
        request_body=NotificationSerializer,
        responses={201: NotificationSerializer()}
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Пометить уведомление как прочитанное",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={"is_read": openapi.Schema(type=openapi.TYPE_BOOLEAN)}
        ),
        responses={200: NotificationSerializer()}
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)
