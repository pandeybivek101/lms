from django.shortcuts import render
from django.utils.safestring import mark_safe
import json
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from .models import *
from account.models import User


def Chat(request):
    return render(request, 'chat/chat.html', {})


def Room(request, room_name):
    return render(request, 'chat/room.html', {
        'room_name_json': mark_safe(json.dumps(room_name)),
        'username':mark_safe(json.dumps(request.user.username))
    })

