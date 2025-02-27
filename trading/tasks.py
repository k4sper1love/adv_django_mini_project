from celery import shared_task
from time import sleep
from notifications.tasks import send_trade_notification, send_websocket_notification


@shared_task
def process_trade(order_id, user_email):
    sleep(5)
    send_trade_notification.delay(user_email, order_id)
    send_websocket_notification(f"Ваш ордер #{order_id} был исполнен!")
    return f"Order {order_id} processed!"
