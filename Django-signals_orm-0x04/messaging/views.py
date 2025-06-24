from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib.auth.models import User
from .models import Message
from django.db.models import Prefetch


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