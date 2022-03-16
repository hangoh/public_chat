from django.shortcuts import redirect, render
import random
from django.http import HttpResponse
from chat.models import ChatRoom
from django.conf import settings
import json
from django.db import transaction

# Create your views here.

numbers = [0,1,2,3,4,5,6,7,8,9]
alphabets = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
generate_code_use=[numbers,alphabets]

def create_room_id():
    room_id=''
    while len(room_id) < 6:
        choices=random.randint(0,1)
        character_choices = random.choice(generate_code_use[choices])
        room_id = room_id+str(character_choices)
    try:
        room = ChatRoom.objects.get(roomId=room_id)
        if room:
            room_id = create_room_id()
            return room_id
    except:
        pass
    return room_id

def home_screen(request):
    if request.POST:
        roomName= request.POST.get('room_name')
        roomId= request.POST.get('room_id')

        #redirect user to chat room when user enter a valid room id
        if roomName == None and not roomId == None:
            context={}
            context['room_id'] = roomId
            try:
                chatroom = ChatRoom.objects.get(roomId = roomId)
                if chatroom:
                    return redirect('chat_screen',roomId=roomId)
            except:
                #redirect user to a error page when user enter a Invalid room id
                return render(request,'room_error.html',context)

        #redirect user to chat room when user create a chat room
        elif roomId==None and not roomName==None :
            if len(roomName)<=30:
                chatRoomId = create_room_id()
                chatroom = ChatRoom.objects.create(name = roomName, roomId = chatRoomId)
                chatroom.save()
                return redirect('chat_screen',roomId=chatRoomId)
    else:
        return render(request,'home.html')

def chat_screen(request,*args, **kwargs):
    context={}
    roomId = kwargs.get('roomId')
    try:
        chatroom = ChatRoom.objects.get(roomId = roomId)
        context['room_id'] =roomId
        context['room_name']= chatroom.name
        context['debug'] = settings.DEBUG

        return render(request,'chat_screen.html',context)
    except:
        context['room_id'] = roomId
        return render(request,'room_error.html',context)

def check_room(request):
    payload={}
    roomId = request.GET.get('roomId')
    print(roomId)
    if roomId:
        try:
            with transaction.atomic():
                room = ChatRoom.objects.select_for_update().get(roomId= roomId)
                if room:
                    payload['response'] = 'got room'
        except:
            payload['response'] = 'no room'
    return HttpResponse(json.dumps(payload),content_type='application/json')