from django.shortcuts import render
from django.views import View 
# Create your views here.


class HomeView(View):
    
    def get(self, request):
        context = {}
        return render(request, template_name='home/home.html', context=context)

        