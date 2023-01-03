# chat application
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import ChatMessageSerializer
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
import json
import requests
from getmac import get_mac_address
from .models import *



@api_view(['POST'])
def send_message(request, room_name):
    serializer = ChatMessageSerializer(data=request.data)
    if serializer.is_valid():
        message = serializer.validated_data['message']
        
        channel_layer = get_channel_layer()
        room_id=RoomName.objects.order_by('-room_name')
        for i in room_id:
            async_to_sync(channel_layer.group_send)(
                f"chat_{room_name}" , {
                    "type": "chat.message", 
                    "message": message,
                    "room_id":str(i.room_name)
                    }
            )
        print(f"chat_{room_name}")
        get,create=RoomName.objects.get_or_create(room_name=f"chat_{room_name}")
        return Response({'message': message})
    return Response(serializer.errors, status=400)






# @api_view(['POST'])
# def send_message(request, room_name):
#     serializer = ChatMessageSerializer(data=request.data)
#     if serializer.is_valid():
#         message = serializer.validated_data['message']
#         print(message)
        
#         ip=request.META.get('REMOTE_ADDR')
#         mac=get_mac_address(ip)
#         ip_address = ip
#         response = requests.get(f'https://ipapi.co/{ip_address}/json/').json()
#         location_data = {
#             "ip": ip_address,
#             "city": response.get("city"),
#             "postal":response.get("postal"),
#             "latitude":response.get("latitude"),
#             "longitude":response.get("longitude"),
#             "region": response.get("region"),
#             "country_capital":response.get("country_capital"),
#             "country": response.get("country_name")
            
#         }
#         print(location_data,"*********************")
    
#         # send the message to the chat consumer here
#         room_id=RoomName.objects.order_by('-room_name')
#         for i in room_id:
    
#             channel_layer = get_channel_layer()
#             async_to_sync(channel_layer.group_send)(
#                 f"chat_{room_name}" , {
#                     "type": "chat.message", 
#                     "message": message,
#                     "room_id":str(i.room_name)
#                     }
#             )
#             print(f"chat_{room_name}")
#             get,create=RoomName.objects.get_or_create(room_name=f"chat_{room_name}")
#             return Response({'message': message, "IP Details":location_data})
#     return Response(serializer.errors, status=400)
