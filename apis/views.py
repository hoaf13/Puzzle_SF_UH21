from django.shortcuts import render
from django.views import View
from django.http import HttpResponse
import wave
# Create your views here.
import logging
import datetime

logger = logging.getLogger(__name__)

def get_timenow_to_int():
    dt = datetime.datetime.now()
    seq = int(dt.strftime("%Y%m%d%H%M%S"))
    return seq

class SaveRecordAPIView(View):
    def get(self, request):
        return HttpResponse("Server save record is running ...")

    def post(self, request):
        logger.debug(f"SaveRecordAPIView - data_file: {request.FILES['data']}")
        audio_data = request.FILES.get('data')
        obj = wave.open(audio_data, 'r')
        file_name = 'audio/' + str(get_timenow_to_int()) + '.wav'        
        audio = wave.open(file_name, 'wb')
        audio.setnchannels(obj.getnchannels())
        audio.setnframes(obj.getnframes())
        audio.setsampwidth(obj.getsampwidth())
        audio.setframerate(obj.getframerate())
        blob = audio_data.read()
        audio.writeframes(blob)
        context = {}
        return render(request, template_name='home/home.html', context=context)    


