import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.conf import settings
import random
import asyncio
import logging 
from utils.records import records
from utils.context import * 

logger = logging.getLogger(__name__)

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
        logger.debug(f"ChatConsumer - add room id: {room_id}")
        logger.debug(f"ChatConsumer - remain_room: {room_ids}")
        self.scope['session']['records'] = records
        self.scope['session']['records']['room_id'] = room_id
        self.scope['session']['records']['session_id'] = self.channel_name
        self.scope['session']['records']['pre_action'] = 'action_start'
        
        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()


    async def disconnect(self, close_code):
        room_id = self.scope['session']['seed'] 
        room_ids.remove(room_id)
        logger.debug(f"remove room id: {room_id}")
        logger.debug(f"remain room ids: {room_ids}")
            
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )


    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
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
        message = event['message'] 
        logger.debug(f"Client message: {message}")
        logger.debug(f"chat message - records first: {self.scope['session']['records']}")        
        records = self.scope['session']['records']
        room_id = self.scope['session']['records']['room_id']
        true_intent = get_true_intent(message, records)
        logger.debug(f"chat_message - true_intent:{true_intent}")
        true_action = get_true_action(true_intent, records)
        logger.debug(f"chat_message - true_action:{true_action}")
        message = get_message_response(message, records, true_intent, true_action)
        self.scope['records'] = update_records(records, true_intent, true_action)
        await self.send(text_data=json.dumps({
            'message': message,
        }))
        