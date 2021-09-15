from django.urls import path
from .views import SaveRecordAPIView
## ENDPOINT: 127.0.0.1/apis/v1/save_record 

urlpatterns = [
    path('save_record/', SaveRecordAPIView.as_view(), name='save-record')
]
