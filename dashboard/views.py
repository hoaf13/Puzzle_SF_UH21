from re import template
from django.shortcuts import render
from django.views import View
from home.models import Conversation, QApair
# Create your views here.

class DashboardView(View):
    def get(self, request):
        convesations = Conversation.objects.all()
        # query get all 
        context = {
            'convertions': convesations
        }    
        return render(request, 'dashboard/index.html', context=context)