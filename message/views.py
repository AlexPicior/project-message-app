from django.shortcuts import render
from message.models import Message, ChatRoom, RecentRooms
from django.contrib.auth.models import User
from django.http import HttpResponse
import json

def chat_friend(request):
    user = request.user
    payload = {}
    if request.method == "POST" and user.is_authenticated:
        partener_id = request.POST.get("partener_id")
        if partener_id:
            partener = User.objects.get(pk=partener_id)
            try:
                new_recent_room = RecentRooms.objects.get(host=user, partener=partener)
                recent_rooms = RecentRooms.objects.filter(host=user)
                
                for recent_room in recent_rooms:
                    recent_room.is_selected = False
                    recent_room.save()
                    
                new_recent_room.is_selected = True
                new_recent_room.save()                           
            except RecentRooms.DoesNotExist:
                try:
                    new_chat_room = ChatRoom.objects.get(user1=user, user2=partener)
                except ChatRoom.DoesNotExist:
                    try:
                        new_chat_room = ChatRoom.objects.get(user1=partener, user2=user)
                    except ChatRoom.DoesNotExist:
                        new_chat_room = ChatRoom(user1=user, user2=partener)
                        new_chat_room.save()
                    
                recent_rooms = RecentRooms.objects.filter(host=user)
                for recent_room in recent_rooms:
                    recent_room.is_selected = False
                    recent_room.save()
                new_recent_room = RecentRooms(host=user, partener=partener, room=new_chat_room, is_selected=True, is_friend=True)
                new_recent_room_partener = RecentRooms(host=partener, partener=user, room=new_chat_room, is_selected=False, is_friend=True)
                
                new_recent_room_partener.save()
                new_recent_room.save()
            
            payload['response'] = 'Chat started successfully.'
                
            if payload['response'] == None:
                payload['response'] = "Something went wrong."
        else:
            payload['response'] = "Unable to start chat."
    else:
        payload['response'] = "You must be authenticated to send a friend request."
    return HttpResponse(json.dumps(payload), content_type="application/json")

def switch_selected(request):
    user = request.user
    payload = {}
    if request.method == "POST" and user.is_authenticated:
        new_selected_id = request.POST.get("new_selected_id")
        if new_selected_id:
            new_selected = RecentRooms.objects.get(pk=new_selected_id)
            recent_rooms = RecentRooms.objects.filter(host=user)
            old_selected_recent_room_id = 0
            old_selected_chat_room_id = 0
            
            for recent_room in recent_rooms:
                if recent_room.is_selected and recent_room.id != new_selected.id:
                    recent_room.is_selected = False
                    recent_room.save()
                    old_selected_recent_room_id = recent_room.id
                    old_selected_chat_room_id = recent_room.room.id
                
                if recent_room.id == new_selected.id:
                    new_selected.is_selected = True
                    new_selected.save()
                    new_selected_recent_room_id = new_selected.id
                    new_selected_chat_room_id = new_selected.room.id
                    
            if old_selected_recent_room_id == 0:
                old_selected_recent_room_id = new_selected_recent_room_id
            
            if old_selected_chat_room_id == 0:
                old_selected_chat_room_id = new_selected_chat_room_id
            
            payload['response'] = 'Switched successfully.'
            payload['new_selected_recent_room_id'] = new_selected_recent_room_id
            payload['old_selected_recent_room_id'] = old_selected_recent_room_id
            payload['new_selected_chat_room_id'] = new_selected_chat_room_id
            payload['old_selected_chat_room_id'] = old_selected_chat_room_id
                
            if payload['response'] == None:
                payload['response'] = "Something went wrong."
        else:
            payload['response'] = "Unable to switch."
    else:
        payload['response'] = "You must be authenticated to send a friend request."
    return HttpResponse(json.dumps(payload), content_type="application/json")
    