from celery import shared_task
from django.core.mail import send_mail

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


@shared_task
def send_trade_notification(email, order_id):
    subject = "Ваш ордер исполнен!"
    message = f"Ваш ордер #{order_id} был успешно обработан."
    send_mail(subject, message, "your_email@gmail.com", [email])
    return f"Notification sent to {email}"

def send_websocket_notification(message):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "notifications",
        {"type": "send_notification", "message": message}
    )
