from django.urls import path
from .views import *

urlpatterns = [
    path('chat/<str:room_name>', send_message)
    
]