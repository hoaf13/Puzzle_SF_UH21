from django.urls import path
from .views import SaveRecordAPIView


urlpatterns = [
    path('save_record/', SaveRecordAPIView.as_view(), name='save-record')
]
