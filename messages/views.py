from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from users.models import User
from .models import Message


@login_required
def message_list(request):
    # Get all unique conversations
    sent_messages = Message.objects.filter(sender=request.user).values_list('receiver', flat=True).distinct()
    received_messages = Message.objects.filter(receiver=request.user).values_list('sender', flat=True).distinct()
    conversation_users = User.objects.filter(
        id__in=list(sent_messages) + list(received_messages)
    ).exclude(id=request.user.id)
    
    return render(request, 'messages/message_list.html', {
        'conversation_users': conversation_users
    })


@login_required
def chat(request, user_id):
    other_user = User.objects.get(id=user_id)
    
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            Message.objects.create(
                sender=request.user,
                receiver=other_user,
                content=content
            )
            return redirect('chat', user_id=user_id)
    
    # Get all messages between current user and other user
    message_list = Message.objects.filter(
        sender__in=[request.user, other_user],
        receiver__in=[request.user, other_user]
    ).order_by('created_at')
    
    # Mark messages as read
    Message.objects.filter(sender=other_user, receiver=request.user, is_read=False).update(is_read=True)
    
    return render(request, 'messages/chat.html', {
        'other_user': other_user,
        'messages': message_list
    })
