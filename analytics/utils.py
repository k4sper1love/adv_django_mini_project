import csv
from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML
from .models import TradeAnalytics


def generate_csv_report():
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="trade_report.csv"'

    writer = csv.writer(response)
    writer.writerow(["Date", "Total Orders", "Total Volume", "Profit/Loss"])

    for report in TradeAnalytics.objects.all():
        writer.writerow([report.date, report.total_orders, report.total_volume, report.profit_loss])

    return response


def generate_pdf_report():
    reports = TradeAnalytics.objects.all()
    html_string = render_to_string("analytics/report_template.html", {"reports": reports})

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="trade_report.pdf"'

    HTML(string=html_string).write_pdf(response)

    return response
