import json
from channels.generic.websocket import AsyncWebsocketConsumer

class TradeConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("trades", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("trades", self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        await self.channel_layer.group_send(
            "trades",
            {
                "type": "trade_update",
                "message": data["message"],
            },
        )

    async def trade_update(self, event):
        await self.send(text_data=json.dumps({"message": event["message"]}))
