import os
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from django.urls import path
from chatapp.consumers import *


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'f_chat.settings')
#application = get_asgi_application()
django_asgi_app = get_asgi_application()

ws_patterns = [
    path('chat/<str:room_name>', ChatConsumer.as_asgi())    
]

application = ProtocolTypeRouter({
     "http": django_asgi_app,
    "websocket": URLRouter(ws_patterns)
    
})