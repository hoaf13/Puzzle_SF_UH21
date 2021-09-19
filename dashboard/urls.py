from django.urls import path
from .views import DashboardView


urlpatterns = [
    path('visualization', DashboardView.as_view(),name='dashboard-view'),
]
