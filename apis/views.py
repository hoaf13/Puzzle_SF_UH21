from django.shortcuts import render
from django.views import View
from django.http import HttpResponse
# Create your views here.

class SaveRecordAPIView(View):
    def get(self, request):
        return HttpResponse("Server save record is running .. ")

    def post(self, request):
        pass    


