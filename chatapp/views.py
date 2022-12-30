# chat application
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import ChatMessageSerializer
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from .consumers import ChatConsumer
import json
import requests
from getmac import get_mac_address



@api_view(['POST'])
def send_message(request, room_name):
    serializer = ChatMessageSerializer(data=request.data)
    if serializer.is_valid():
        message = serializer.validated_data['message']
        if message is not None:
            ip=request.META.get('REMOTE_ADDR')
            mac=get_mac_address(ip)
            ip_address = ip
            response = requests.get(f'https://ipapi.co/{ip_address}/json/').json()
            location_data = {
                "ip": ip_address,
                "city": response.get("city"),
                "region": response.get("region"),
                "country": response.get("country_name")
            }
            print(location_data,"*********************")
        
            # send the message to the chat consumer here
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                f"chat_{room_name}" , {
                    "type": "chat.message", 
                    "message": message,
                    "ip":ip,
                    "mac":mac,
                    }
            )
            return Response({'message': message})
    return Response(serializer.errors, status=400)
