from django.db import models
from trading.models import Order

class TradeAnalytics(models.Model):
    date = models.DateField(auto_now_add=True)
    total_orders = models.IntegerField(default=0)
    total_volume = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    profit_loss = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)

    def __str__(self):
        return f"Analytics for {self.date}"
