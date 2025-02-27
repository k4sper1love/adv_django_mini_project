from django.urls import path
from .views import TradeAnalyticsView, download_csv_report, download_pdf_report

urlpatterns = [
    path("analytics/", TradeAnalyticsView.as_view(), name="trade-analytics"),
    path("analytics/report/csv/", download_csv_report, name="download-csv-report"),
    path("analytics/report/pdf/", download_pdf_report, name="download-pdf-report"),
]
