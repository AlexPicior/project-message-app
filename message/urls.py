from django.urls import path
from message.views import (
    chat_friend,
    switch_selected,
)

app_name = 'message'

urlpatterns = [
    path('chat_with_friend/', chat_friend, name='chat-with-friend'),
    path('switch_selected/', switch_selected, name='switch-selected'),
]