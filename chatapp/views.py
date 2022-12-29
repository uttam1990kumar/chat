# chat application
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import ChatMessageSerializer
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from .consumers import ChatConsumer




@api_view(['POST'])
def send_message(request, room_name):
    serializer = ChatMessageSerializer(data=request.data)
    if serializer.is_valid():
        message = serializer.validated_data['message']
        
        # send the message to the chat consumer here
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"chat_{room_name}" , {
                "type": "chat.message", 
                "message": message,
                }
        )
        return Response({'message': message})
    return Response(serializer.errors, status=400)
