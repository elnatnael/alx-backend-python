from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib.auth.models import User
from .models import Message
from django.db.models import Prefetch
from django.shortcuts import render


@login_required
def delete_user(request):
    user = request.user
    user.delete()
    return redirect('home')  # 👈 redirect somewhere appropriate

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