from django.urls import path
from chat.views import home_screen,chat_screen,check_room

urlpatterns = [
    path('',home_screen,name='home_screen'),
    path('<roomId>/',chat_screen,name='chat_screen'),
    path('check_room/',check_room,name='check_room')
]
