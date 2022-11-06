from django.contrib import admin
from friend.models import FriendList, FriendRequest
from message.models import Message, ChatRoom, RecentRooms

class FriendListAdmin(admin.ModelAdmin):
    list_filter = ['user']
    list_display = ['user']
    search_fields = ['user']
    readonly_fields = ['user']

    class Meta:
        model = FriendList
    
admin.site.register(FriendList, FriendListAdmin)

class FriendRequestAdmin(admin.ModelAdmin):
    list_filter = ['sender', 'receiver']
    list_display = ['sender', 'receiver']
    search_fields = ['sender__username', 'receiver__username']

    class Meta:
        model = FriendRequest

admin.site.register(FriendRequest, FriendRequestAdmin)

class MessageAdmin(admin.ModelAdmin):
    list_filter = ['messager']
    list_display = ['messager']
    search_fields = ['messager']
    readonly_fields = ['messager']
    
    class Meta:
        model = Message

admin.site.register(Message, MessageAdmin)

class ChatRoomAdmin(admin.ModelAdmin):
    list_filter = ['user1', 'user2']
    list_display = ['user1', 'user2']
    search_fields = ['user1__username', 'user2__username']
    
    class Meta:
        model = ChatRoom
        
admin.site.register(ChatRoom, ChatRoomAdmin)

class RecentRoomsAdmin(admin.ModelAdmin):
    list_filter = ['host', 'partener']
    list_display = ['host', 'partener']
    search_fields = ['host__username', 'partener__username']
    
    class Meta:
        model = RecentRooms

admin.site.register(RecentRooms, RecentRoomsAdmin)