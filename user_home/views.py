from django.shortcuts import render
from django.contrib.auth.decorators import login_required 
from django.contrib.auth.models import User
from friend.models import FriendRequest
from friend.models import FriendList
from message.models import RecentRooms, ChatRoom

@login_required(login_url='/login')
def user_home(request):
    context = {}
    user = request.user
    the_selected = False
    recent_roomss = RecentRooms.objects.filter(host=user, is_friend=True)
    recent_rooms = []
    for recent_room in recent_roomss:
        if recent_room.is_selected:
            the_selected = recent_room
        recent_rooms.append(recent_room)
    
    def sorting_fun(e):
        return e.id
    
    recent_rooms.sort(key=sorting_fun)
    context['the_selected'] = the_selected
    context['recent_rooms'] = recent_rooms
    
    chat_rooms = []
    chat_rooms1 = ChatRoom.objects.filter(user1=user)
    chat_rooms2 = ChatRoom.objects.filter(user2=user)
    if chat_rooms1:
        for chat_room1 in chat_rooms1:
            messages = []
            for message in chat_room1.messages.all():
                messages.append(message)
            messages.reverse()
            chat_rooms.append((chat_room1, messages))
    if chat_rooms2:
        for chat_room2 in chat_rooms2:
            messages = []
            for message in chat_room2.messages.all():
                messages.append(message)
            messages.reverse()
            chat_rooms.append((chat_room2, messages))
    context['chat_rooms'] = chat_rooms
    
    return render(request, 'messages.html', context)

@login_required(login_url='/login')
def friends(request):
    user = request.user
    context = {}
    friend_list = FriendList.objects.get(user=user)
    friends = []
    searched_friends = []
    
    if request.method == 'GET':
        search_query = request.GET.get("q")
        if search_query:
            if len(search_query) > 0:
                search_results = friend_list.friends.filter(username__icontains = search_query)
                if search_results:
                    context['search_result'] = True
                    for friend in search_results:
                        searched_friends.append(friend)
                else:
                    context['search_result'] = False
        else:
            context['search_result'] = True 
            for friend in friend_list.friends.all():
                friends.append(friend)
    
    
    context['friends'] = friends
    context['searched_friends'] = searched_friends
    
    return render(request,'friends.html', context)

@login_required(login_url='/login')
def notifications(request):
    context = {}
    user = request.user
    friend_requests = FriendRequest.objects.filter(receiver=user, is_active=True)
    context['friend_requests'] = friend_requests
    return render(request, 'notifications.html', context)

@login_required(login_url='/login')
def add_friend(request):
    context = {}
    context['other_friend_request_id'] = 1
    user = request.user

    if request.method == 'GET':
        search_query = request.GET.get("q")
        if search_query:
            if len(search_query) > 0:
                search_results = User.objects.filter(username__icontains = search_query)
                accounts = []
                
                if user.is_authenticated:
                    friend_list = FriendList.objects.get(user=user)
                    for account in search_results:
                        is_friend_request_active = False
                        sent_by_other = False
                        try:
                            other_friend_request = FriendRequest.objects.get(sender=account, receiver=user)
                            if other_friend_request.is_active:
                                sent_by_other = True
                                context['other_friend_request_id'] = other_friend_request.id
                            else:
                                try:
                                    friend_request = FriendRequest.objects.get(sender=user, receiver=account) 
                                    if friend_request.is_active:
                                        is_friend_request_active = True
                                except FriendRequest.DoesNotExist:
                                    is_friend_request_active = False
                        except FriendRequest.DoesNotExist:
                            try:
                                friend_request = FriendRequest.objects.get(sender=user, receiver=account) 
                                if friend_request.is_active:
                                    is_friend_request_active = True
                            except FriendRequest.DoesNotExist:
                                is_friend_request_active = False
                            
                        accounts.append((account, friend_list.is_mutual_friend(account), is_friend_request_active, sent_by_other))
                else:
                    for account in search_results:
                        is_friend_request_active = False
                        sent_by_other = False
                        try:
                            friend_request = FriendRequest.objects.get(sender=user, receiver=account) 
                            if friend_request.is_active:
                                is_friend_request_active = True
                        except FriendRequest.DoesNotExist:
                            is_friend_request_active = False
                            
                        accounts.append((account, False, is_friend_request_active, sent_by_other))
                        
                context['accounts'] = accounts
    return render(request, 'add_friend.html', context)


                