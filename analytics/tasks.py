from celery import shared_task
from django.utils.timezone import now
from trading.models import Order
from .models import TradeAnalytics

@shared_task
def generate_daily_trade_report():
    today = now().date()
    orders = Order.objects.filter(created_at__date=today)
    total_orders = orders.count()
    total_volume = sum(order.amount for order in orders)
    profit_loss = sum(order.profit_loss for order in orders if hasattr(order, 'profit_loss'))

    report, created = TradeAnalytics.objects.get_or_create(date=today)
    report.total_orders = total_orders
    report.total_volume = total_volume
    report.profit_loss = profit_loss
    report.save()

    return f"Report generated for {today}: {total_orders} orders, volume {total_volume}, P/L {profit_loss}"
