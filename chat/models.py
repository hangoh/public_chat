from django.db import models
from django.db.models.aggregates import Min

# Create your models here.
class ChatRoom(models.Model):
    name = models.CharField(max_length=30)
    roomId = models.CharField(max_length=6)
    connection_number = models.IntegerField(default=0)
    
    def __str__(self):
        return self.name

class RoomMessage(models.Model):
    sender = models.CharField(max_length=300)
    message = models.TextField(blank=False, null=False)
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return ('{} ({})').format(self.sender, self.room.name)