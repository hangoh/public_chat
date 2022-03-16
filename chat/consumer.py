from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async
from django.core import paginator
from django.db.models.fields import NullBooleanField
from chat.models import ChatRoom, RoomMessage
from django.db import transaction
from django.core.paginator import Paginator
from chat.utils import RoomMessagesSerializer
from django.core.serializers import serialize
import json

class ChatRoomConsumer(AsyncJsonWebsocketConsumer):
   

    async def connect(self):
        await self.accept()
        self.roomId=None
    
    async def disconnect(self, code):
        await minus_one_to_connection_number(self.roomId)
        await track_room_connection_number(self.roomId)
        self.roomId=None

    async def receive_json(self, content, **kwargs):
        command = content.get('command',None)
        try:
            if command == 'join':
                await plus_one_to_connection_number(content['roomId'])
                room = await find_room(content['roomId'])
                if room:
                    number_user = await get_number_user(content['roomId'])
                    print(number_user)
                    await self.join_room(content['roomId'])
            
            if command == 'send_message':
                room = await find_room(content['roomId'])
                payload = await create_chat_message(sender = content['username'],message = content['message'], room =room)

                if payload:
                    payload = json.loads(payload)
                    print(payload)
                    await self.send_message(room=room , username=content['username'], message=payload['message'] )
            
            if command == 'get_previous_chat':
                room = await find_room(content['roomId'])
                if room:
                    payload = await get_chat(room, content['page_number'])
                    if payload!=None:
                        payload = json.loads(payload)
                        await self.send_previous_messages(payload['messages'], payload['new_page_number'])
         

        except:
            pass

    async def join_room(self,room_id):
        self.roomId=room_id
        room = await find_room(room_id)
        if room != None: 
            await self.channel_layer.group_add(
                room.name,
                self.channel_name
            )
            
            await self.channel_layer.group_send(
                room.name,
                {
                    'type':'room_join',
                    
                }
            )

    async def room_join(self, event):
        await self.send_json({
            'content':'join_success',
            
        })
    
   
    async def send_message(self,room,username,message):
        if room:
            await self.channel_layer.group_send(
                room.name,
                {
                    'type':'room.message',
                    'username':username,
                    'message':message,
                    
                }
            )
            
    
    async def room_message(self,event):
        await self.send_json({
            'content':'chat_message',
            'username':event['username'],
            'message':event['message'],
            
        })
    
    async def send_previous_messages(self,messages, new_page_number):
        await self.send_json({
            'content':'previous_messages',
            'messages':messages,
            'new_page_number':new_page_number
        })
    
    
    
@database_sync_to_async
def find_room(roomId):
    try:
        room = ChatRoom.objects.get(roomId = roomId)
        if room:
            return room
    except:
        return None

@database_sync_to_async
def get_number_user(roomId):
    try:
        room = ChatRoom.objects.get(roomId = roomId)
        if room:
            return int(room.connection_number)
    except:
        return None


@database_sync_to_async
def plus_one_to_connection_number(roomId):
    try:
        with transaction.atomic():
            room = ChatRoom.objects.select_for_update().get(roomId = roomId)
            if room:
                room.connection_number+=1
                room.save()
    except:
        pass

@database_sync_to_async
def minus_one_to_connection_number(roomId):
    try:
        with transaction.atomic():
            room = ChatRoom.objects.select_for_update().get(roomId = roomId)
            if room:
                room.connection_number-=1
                room.save()
    except:
        pass

@database_sync_to_async
def track_room_connection_number(roomId):
    try:
        with transaction.atomic():
            room = ChatRoom.objects.select_for_update().get(roomId=roomId)
            if room.connection_number <1:
                room.delete()
            else:
                pass
    except:
        pass

@database_sync_to_async
def create_chat_message(sender,message,room):
    if len(message) > 1 :
        chatMessage = RoomMessage.objects.create(sender = sender, message=message, room = room)
        chatMessage.save()
        payload = {}
        s = RoomMessagesSerializer()
        payload['message'] = s.serialize([chatMessage])[0]
        return json.dumps(payload)
    else:
        return False

@database_sync_to_async
def get_chat(room, page_number):
    try:
        messages = RoomMessage.objects.filter(room = room).order_by('-timestamp')
        p = Paginator(messages,20)
        payload={}
        new_page_number = int(page_number)
       
        if new_page_number <= p.num_pages:
            payload['new_page_number'] = new_page_number+1
            s = RoomMessagesSerializer()
            payload['messages'] = s.serialize(p.page(page_number).object_list)
            return json.dumps(payload)
        else:
            return None
    except:
        return None
        