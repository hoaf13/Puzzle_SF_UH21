import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.conf import settings
import random
import asyncio
room_ids = set()

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        room_id = random.randint(1, 1000)
        while room_id in room_ids:
            room_id = random.randint(1, 1000)
        room_ids.add(room_id)
        self.scope['session']['seed'] = room_id
        self.room_name = room_id
        self.room_group_name = 'chat_%s' % self.room_name
        print(f"add room id: {room_id}")
        print("remain", room_ids)
        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        room_id = self.scope['session']['seed'] 
        room_ids.remove(room_id)
        print(f"remove room id: {room_id}")
        print("remain: ", room_ids)

        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        print("client: ", message)
        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message'] + "tin nhan 1"
        await self.send(text_data=json.dumps({
            'message': message
        }))
        
        message = event['message'] + "tin nhan 2"
        await self.send(text_data=json.dumps({
            'message': message
        }))
        