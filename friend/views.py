from re import T
from django.shortcuts import render
from friend.models import FriendList
from friend.models import FriendRequest
from message.models import RecentRooms
from django.contrib.auth.models import User
from django.http import HttpResponse
import json

def send_friend_request(request, *args, **kwargs):
	user = request.user
	payload = {}
	if request.method == "POST" and user.is_authenticated:
		user_id = request.POST.get("receiver_user_id")
		if user_id:
			receiver = User.objects.get(pk=user_id)
			try:
				friend_request = FriendRequest.objects.get(sender=user, receiver=receiver)
				try:
					if friend_request.is_active:
						raise Exception("You already sent them a friend request.")
					else:
						friend_request.is_active = True
						friend_request.save()
					payload['response'] = "Friend request sent."
				except Exception as e:
					payload['response'] = str(e)
			except FriendRequest.DoesNotExist:
				friend_request = FriendRequest(sender=user, receiver=receiver)
				friend_request.save()
				payload['response'] = "Friend request sent."

			if payload['response'] == None:
				payload['response'] = "Something went wrong."
		else:
			payload['response'] = "Unable to sent a friend request."
	else:
		payload['response'] = "You must be authenticated to send a friend request."
	return HttpResponse(json.dumps(payload), content_type="application/json")

def accept_friend_request(request, *args, **kwargs):
    user = request.user
    payload = {}
    
    if request.method == "GET" and user.is_authenticated:
        friend_request_id = kwargs.get("friend_request_id")
        if friend_request_id:
            friend_request = FriendRequest.objects.get(pk=friend_request_id)
            if friend_request.receiver == user:
                partener = friend_request.sender
                if friend_request:
                    friend_request.accept()
                    try:
                        recent_room_user = RecentRooms.objects.get(host=user, partener=partener)
                        recent_room_user.is_friend = True
                        recent_room_user.save()
                        try:
                            recent_room_partener = RecentRooms.objects.get(host=partener, partener=user)
                            recent_room_partener.is_friend = True
                            recent_room_partener.save()
                        except RecentRooms.DoesNotExist:
                            pass
                    except RecentRooms.DoesNotExist:
                        try:
                            recent_room_partener = RecentRooms.objects.get(host=partener, partener=user)
                            recent_room_partener.is_friend = True
                            recent_room_partener.save()
                        except RecentRooms.DoesNotExist:
                            pass
                    payload['response'] = "Friend request accepted."
                else:
                    payload['response'] = "Something went wrong."
            elif friend_request.sender == user:
                partener = friend_request.receiver
                if friend_request:
                    friend_request.accept()
                    try:
                        recent_room_user = RecentRooms.objects.get(host=user, partener=partener)
                        recent_room_user.is_friend = True
                        recent_room_user.save()
                        try:
                            recent_room_partener = RecentRooms.objects.get(host=partener, partener=user)
                            recent_room_partener.is_friend = True
                            recent_room_partener.save()
                        except RecentRooms.DoesNotExist:
                            pass
                    except RecentRooms.DoesNotExist:
                        try:
                            recent_room_partener = RecentRooms.objects.get(host=partener, partener=user)
                            recent_room_partener.is_friend = True
                            recent_room_partener.save()
                        except RecentRooms.DoesNotExist:
                            pass
                    payload['response'] = "Friend request accepted."
                else:
                    payload['response'] = "Something went wrong."
            else:
                payload['response'] = "That is not your request to accept."
        else:
            payload['response'] = "Unable to accept that friend request."
    else:
        payload['response'] = "You must be authenticated to accept a friend request."
    return HttpResponse(json.dumps(payload), content_type="application/json")

def remove_friend(request, *args, **kwargs):
	user = request.user
	payload = {}
	if request.method == "POST" and user.is_authenticated:
		user_id = request.POST.get("receiver_user_id")
		if user_id:
			try:
				removee = User.objects.get(pk=user_id)
				friend_list = FriendList.objects.get(user=user)
				friend_list.unfriend(removee)
    
				try:
					recent_room_user = RecentRooms.objects.get(host=user, partener=removee)
					recent_room_user.is_friend = False
					recent_room_user.save()
					try:
						recent_room_removee = RecentRooms.objects.get(host=removee, partener=user)
						recent_room_removee.is_friend = False
						recent_room_removee.save()
					except RecentRooms.DoesNotExist:
						pass
				except RecentRooms.DoesNotExist:
					try:
						recent_room_removee = RecentRooms.objects.get(host=removee, partener=user)
						recent_room_removee.is_friend = False
						recent_room_removee.save()
					except RecentRooms.DoesNotExist:
						pass
  
				payload['response'] = "Successfully removed that friend."
			except Exception as e:
				payload['response'] = f"Something went wrong: {str(e)}"
		else:
			payload['response'] = "There was an error. Unable to remove that friend."
	else:
		payload['response'] = "You must be authenticated to remove a friend."
	return HttpResponse(json.dumps(payload), content_type="application/json")

def decline_friend_request(request, *args, **kwargs):
	user = request.user
	payload = {}
	if request.method == "GET" and user.is_authenticated:
		friend_request_id = kwargs.get("friend_request_id")
		if friend_request_id:
			friend_request = FriendRequest.objects.get(pk=friend_request_id)
			if friend_request.receiver == user:
				if friend_request: 
					friend_request.decline()
					payload['response'] = "Friend request declined."
				else:
					payload['response'] = "Something went wrong."
			else:
				payload['response'] = "That is not your friend request to decline."
		else:
			payload['response'] = "Unable to decline that friend request."
	else:
		# should never happen
		payload['response'] = "You must be authenticated to decline a friend request."
	return HttpResponse(json.dumps(payload), content_type="application/json")

def cancel_friend_request(request, *args, **kwargs):
	user = request.user
	payload = {}
	if request.method == "POST" and user.is_authenticated:
		user_id = request.POST.get("receiver_user_id")
		if user_id:
			receiver = User.objects.get(pk=user_id)
			try:
				friend_requests = FriendRequest.objects.filter(sender=user, receiver=receiver, is_active=True)
			except FriendRequest.DoesNotExist:
				payload['response'] = "Nothing to cancel. Friend request does not exist."

			if len(friend_requests) > 1:
				for request in friend_requests:
					request.cance()
				payload['response'] = "Friend request canceled."
			else:
				friend_requests.first().cancel()
				payload['response'] = "Friend request canceled."
		else:
			payload['response'] = "Unable to cancel that friend request."
	else:
		payload['response'] = "You must be authenticated to cancel a friend request."
	return HttpResponse(json.dumps(payload), content_type="application/json")