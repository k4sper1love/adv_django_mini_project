from rest_framework.generics import ListAPIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import permissions
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import TradeAnalytics
from .serializers import TradeAnalyticsSerializer
from .utils import generate_csv_report, generate_pdf_report

class TradeAnalyticsView(ListAPIView):
    queryset = TradeAnalytics.objects.all()
    serializer_class = TradeAnalyticsSerializer
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Получить список аналитики по торгам",
        responses={200: TradeAnalyticsSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

@swagger_auto_schema(
    method="get",
    operation_description="Скачать CSV-отчет по торгам",
    responses={200: openapi.Response("CSV-файл с отчетом")}
)
@api_view(["GET"])
def download_csv_report(request):
    return generate_csv_report()

@swagger_auto_schema(
    method="get",
    operation_description="Скачать PDF-отчет по торгам",
    responses={200: openapi.Response("PDF-файл с отчетом")}
)
@api_view(["GET"])
def download_pdf_report(request):
    return generate_pdf_report()
