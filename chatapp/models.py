from django.db import models

# Create your models here.

class RoomName(models.Model):
    room_name=models.CharField(max_length=50)