from django.http.response import HttpResponse
from django.shortcuts import render
from django.views import View 
from django.shortcuts import redirect
import logging
# Create your views here.
import wave
import datetime 
import requests
import json
from utils.context import * 
from utils.records import records as init_record
import redis 
from utils import records

red = redis.StrictRedis(host='localhost', port=6379)

logger = logging.getLogger(__name__)

f = open('config/api_config.json','r')
API_CONFIG = json.load(f)
STT_ENDPOINT = API_CONFIG['voice-api'][0]['endpoint']
STT_TOKEN = API_CONFIG['voice-api'][0]['token']
TTS_ENDPOINT = API_CONFIG['voice-api'][1]['endpoint']
TTS_TOKEN = API_CONFIG['voice-api'][1]['token']

logger.debug(f"STT ENDPOINT: {STT_ENDPOINT}")
logger.debug(f"STT TOKEN: {STT_TOKEN}")
logger.debug(f"TTS ENDPOINT: {TTS_ENDPOINT}")
logger.debug(f"TTS TOKEN: {TTS_TOKEN}")

def get_timenow_to_int():
    dt = datetime.datetime.now()
    seq = int(dt.strftime("%Y%m%d%H%M%S"))
    return seq

def download(url, file_name):
    with open(file_name, "wb") as file:
        response = requests.get(url)
        file.write(response.content)

logger = logging.getLogger(__name__)

class HomeView(View):
    
    def get(self, request):
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
        audio_url = init_record['audio_tts_url']
        context = {}
        if audio_url != None:
            context = {
                "audio_url": audio_url
            }
        logger.debug(f"HomeView - audio_url: {audio_url}")
        return render(request, template_name='home/home.html', context=context)
        

    def post(self, request):
        # save audio from websocket
        audio_data = request.FILES.get('data')
        filename = str(audio_data)
        logger.debug(f"HomeView - audio_data filename:{filename}")
        obj = wave.open(audio_data, 'r')
        saved_file = 'resource/audio/' + filename + '.wav'        
        audio = wave.open(saved_file, 'wb')
        audio.setnchannels(obj.getnchannels())
        audio.setnframes(obj.getnframes())
        audio.setsampwidth(obj.getsampwidth())
        audio.setframerate(obj.getframerate())
        blob = audio_data.read()
        audio.writeframes(blob)
        logger.debug(f"HomeView - save audio file successfully !")
        
        # request to STT
        stt_token = {
            "token": STT_TOKEN,
        }
        stt_files = {
            "audio-file": open(saved_file,'rb')
        }
        stt_response = requests.post(STT_ENDPOINT, data=stt_token, files=stt_files).text
        logger.debug(f"HomeView - stt_response: {stt_response}")
        stt_message = json.loads(stt_response)['result']['text']
        logger.debug(f"- [TTS Client Message]: {stt_message}")
        
        # NLP processing
        true_intent = get_true_intent(stt_message, init_record)
        logger.debug(f"HomeView - true_intent:{true_intent}")
        true_action = get_true_action(true_intent, init_record)
        logger.debug(f"HomeView - true_action:{true_action}")
        bot_response = get_message_response(stt_message, init_record, true_intent, true_action, flag="text_tts")
        update_records(init_record, true_intent, true_action)
        logger.debug(f"HomeView - bot_response: {bot_response}")
        
        # request to TTS
        tts_data = {
            "token": TTS_TOKEN,
            "text": bot_response,
            "voiceId": 11
        }
        tts_response = requests.post(TTS_ENDPOINT, data=tts_data).text
        logger.debug(f"- [TTS Bot Message]: {bot_response}")
        audio_url = json.loads(tts_response)['data']['url']
        logger.debug(f"HomeView - url_audio: {audio_url}")
        saved_file_tts = 'resource/audio_tts/' + filename + '.wav'
        download(url=audio_url, file_name=saved_file_tts)
        logger.debug(f"HomeView - save file tts successfully!") 
        init_record['audio_tts_url'] = audio_url        
        red.set(filename, audio_url)
        logger.debug(f"HomveView - set filename: {filename} to redis successfully... ")

        return redirect('home-view')


