import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import User

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # self.room_name = "message"
        # self.room_group_name = "chat_"+self.room_name
        
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}" 
        
        
        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name, 
            self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name, 
            self.channel_name
            )

    # Receive message from WebSocket
    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data["message"]

        # Send message to room group
        # username=User.objects.order_by()[0]   
        # if username is not None:
        # await self.channel_layer.group_send(
        #     self.room_group_name, {
        #         "type": "chat.message"
        #         "message": message})
        # await self.send(text_data=json.dumps({"Admin":message}))
        

    # Receive message from room group
    async def chat_message(self, event):
        message = event["message"]
        
        # #Send message to WebSocket
        await self.send(text_data=json.dumps({"message": message}))
