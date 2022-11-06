from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from friend.models import FriendList

# Create your views here.

def sign_up(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            new_friend_list = FriendList(user=user)
            new_friend_list.save()
            login(request, user)
            return redirect('/home')
    else:
        form = UserCreationForm()
        
    return render(request, 'sign_up.html', {'form': form})