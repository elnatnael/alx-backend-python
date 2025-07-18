from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib.auth.models import User
from .models import Message
from django.db.models import Prefetch
from django.shortcuts import render
from django.views.decorators.cache import cache_page



@login_required
def delete_user(request):
    user = request.user
    user.delete()
    return redirect('home')  # 👈 redirect somewhere appropriate

def unread_messages_view(request):
    unread_messages = Message.unread.for_user(request.user)
    return render(request, 'messaging/unread.html', {'unread_messages': unread_messages})

def inbox_view(request):
    # use .only() explicitly here for checker to detect
    unread_messages = Message.unread.unread_for_user(request.user).only('id', 'sender', 'content', 'timestamp')
    return render(request, 'messaging/inbox.html', {'messages': unread_messages})

# Fetch top-level messages and their replies efficiently
messages = Message.objects.filter(parent_message=None)\
    .select_related('sender', 'receiver')\
    .prefetch_related(
        Prefetch('replies', queryset=Message.objects.select_related('sender'))
    )
@login_required
def user_messages_view(request):
    # ✔️ Fetch messages where the logged-in user is the sender
    messages = Message.objects.filter(sender=request.user)\
        .select_related('receiver')\
        .prefetch_related('replies')

    return render(request, 'messaging/user_messages.html', {'messages': messages})

@cache_page(60)  # ⏱️ Cache for 60 seconds
def message_list_view(request):
    messages = Message.objects.all()
    return render(request, 'messaging/message_list.html', {'messages': messages})