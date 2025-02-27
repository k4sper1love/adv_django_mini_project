from django.contrib import admin
from .models import Order, Transaction

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "product", "quantity", "status")
    search_fields = ("user__username", "product__name")
    list_filter = ("status",)

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ("id", "order", "amount", "transaction_date")
    search_fields = ("order__id",)
