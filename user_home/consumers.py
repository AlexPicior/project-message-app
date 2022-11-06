import json
from tokenize import group
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from message.models import ChatRoom, Message
from django.contrib.auth.models import User


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        user = self.scope['user']
        chat_rooms = []
        chat_rooms1 = ChatRoom.objects.filter(user1=user)
        chat_rooms2 = ChatRoom.objects.filter(user2=user)
        for chat_room in chat_rooms1:
            chat_rooms.append(chat_room)
        for chat_room in chat_rooms2:
            chat_rooms.append(chat_room)
            
        for chat_room in chat_rooms:
            async_to_sync(self.channel_layer.group_add)(
                str(chat_room.id),
                self.channel_name
            )

        self.accept()
        
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        group_name = text_data_json['group_name']
        sender_username = text_data_json['sender_username']
        
        sender = User.objects.get(username=sender_username)
        new_message = Message(messager=sender, text=str(message))
        new_message.save()
        chat_room = ChatRoom.objects.get(pk=group_name)
        chat_room.add_message(new_message)

        async_to_sync(self.channel_layer.group_send)(
            group_name,
            {
                'type': 'chat_message',
                'message': message,
                'chat_room_id':group_name,
                'sender_username':sender_username,
            }
        )
    
    def chat_message(self, event):
        message = event['message']
        group_name = event['chat_room_id']
        sender_username = event['sender_username']

        self.send(text_data=json.dumps({
            'type':'chat',
            'message': message,
            'chat_room_id':group_name,
            'sender_username':sender_username,
        }))