from django.shortcuts import render
from django.views import View
from django.http import HttpResponse
import wave
# Create your views here.

class SaveRecordAPIView(View):
    def get(self, request):
        return HttpResponse("Server save record is running .. ")

    def post(self, request):
        print((request.FILES['data']))
        audio_data = request.FILES.get('data')
        obj = wave.open(audio_data, 'r')
        print(obj)
        audio = wave.open('test.wav', 'wb')
        audio.setnchannels(obj.getnchannels())
        audio.setnframes(obj.getnframes())
        audio.setsampwidth(obj.getsampwidth())
        audio.setframerate(obj.getframerate())
        blob = audio_data.read()
        audio.writeframes(blob)
        context = {}
        return render(request, template_name='home/home.html', context=context)    


