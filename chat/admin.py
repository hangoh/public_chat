from django.contrib import admin
from chat.models import ChatRoom, RoomMessage
# Register your models here.


class ChatRoomAdmin(admin.ModelAdmin):
    list_display=['name','roomId','id']
    readonly_fields=['id']
    list_filter=['name']
    search_fields=['name','roomId','id']

class RoomMessageAdmin(admin.ModelAdmin):
    list_display=['sender','message','room','timestamp','id']
    readonly_fields=['timestamp','id']
    list_filter=['sender','room']
    search_fields=['sender','room']


admin.site.register(ChatRoom,ChatRoomAdmin)
admin.site.register(RoomMessage,RoomMessageAdmin)