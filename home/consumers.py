import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.conf import settings
import random
import logging
import redis
from numpy.core.shape_base import block 
from utils.records import records
from utils.context import * 
import urllib.request as request
import time 
import os 
import asyncio

red = redis.StrictRedis(host='localhost', port=6379)

logger = logging.getLogger(__name__)
room_ids = set()

def download(url, file_name):
    with open(file_name, "wb") as file:
        response = requests.get(url)
        file.write(response.content)

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
        records = {
            "room_id": None,
            "pre_action": None,
            "pre_intent": None,
            "cur_action": None,
            "cur_intent": None,
            "time_repeat": 0,
            "confirm_repeat": 0,

            "hospital_name": "Hồng Ngọc",
            "choosen_department": None,
            "customer_name": None,
            "customer_age": None,
            "customer_gender": None, 
            "customer_symptom": None,
            "customer_pick_date": None, 
            "customer_pick_date_detail": None, 
            "is_priority": None,
            "department": None,
            "free_date": None,
            "this_week_free_date_status": None,
            "repeat_action": 0
        }
        self.scope['session']['records'] = records
        self.scope['session']['records']['room_id'] = room_id
        self.scope['session']['records']['session_id'] = self.channel_name
        self.scope['session']['records']['pre_action'] = 'action_start'
        records['pre_action'] = 'action_start'
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
        logger.debug(f"receive from socket: {text_data_json}")
        text_data_json = text_data_json['message']
        message = text_data_json['message']
        input_type = text_data_json['input_type']
        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'input_type': input_type
            }
        )


    # Receive message from room group
    async def chat_message(self, event):
        message = event['message'] 
        input_type = event['input_type']
        logger.debug(f"ChatConsumer - input_type: {input_type}")

        if input_type == 'button':
            logger.debug(f"ChatConsumer - client message: {message}")
            logger.debug(f"ChatConsumer - records first: {self.scope['session']['records']}")        
            records = self.scope['session']['records']
            true_intent = get_true_intent(message, records)
            logger.debug(f"ChatConsumer - true_intent:{true_intent}")
            true_action = get_true_action(true_intent, records)
            logger.debug(f"ChatConsumer - true_action:{true_action}")
            message = get_message_response(message, records, true_intent, true_action)
            self.scope['records'] = update_records(records, true_intent, true_action)
            await self.send(text_data=json.dumps({
                'message': message,
                'input_type': 'button'
            }))

        if input_type == 'logo':
            filename = message 
            while True:
                await asyncio.sleep(1)
                value = red.get(filename)
                logger.debug(f"value: {value}")
                if value:
                    break
            audio_url = red.get(filename).decode("utf-8") 
            logger.debug(f"----Send audio url: {audio_url}")
            await self.send(
              text_data=json.dumps({
                'audio_url': audio_url,
                'input_type': 'logo'
                })  
            )