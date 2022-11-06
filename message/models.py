from email import message
from django.db import models
from django.contrib.auth.models import User

class Message(models.Model):
    messager = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messager')
    text = models.TextField(null=False, blank=False)

class ChatRoom(models.Model):
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user1')
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user2')
    messages = models.ManyToManyField(Message, blank=True, related_name='messages')
    
    def add_message(self, message):
        self.messages.add(message)
        self.save()
    
class RecentRooms(models.Model):
    host = models.ForeignKey(User, on_delete=models.CASCADE, related_name='host')
    partener = models.ForeignKey(User, on_delete=models.CASCADE, related_name='partener')
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='room')
    is_selected = models.BooleanField(blank=True, null=False, default=True)
    is_friend = models.BooleanField(blank=True, null=False, default=True)

