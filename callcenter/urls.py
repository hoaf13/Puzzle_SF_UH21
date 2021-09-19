from django.urls import path
from .views import CallcenterView

urlpatterns = [
    path('', CallcenterView.as_view(), name='callcenter-view')
]
