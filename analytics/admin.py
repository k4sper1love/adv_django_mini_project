from django.contrib import admin
from .models import SalesOrder, Invoice

@admin.register(SalesOrder)
class SalesOrderAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "product", "quantity", "total_price", "status")
    search_fields = ("user__username", "product__name")
    list_filter = ("status",)

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ("id", "sales_order", "invoice_number", "issued_at")
    search_fields = ("invoice_number",)
