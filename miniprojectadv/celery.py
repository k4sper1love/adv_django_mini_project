import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sales_trading.settings")

app = Celery("sales_trading")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

app.conf.beat_schedule = {
    "generate_daily_trade_report": {
        "task": "analytics.tasks.generate_daily_trade_report",
        "schedule": crontab(hour=23, minute=59),
    },
}
