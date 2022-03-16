from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.urls import path
from chat.consumer import ChatRoomConsumer

application = ProtocolTypeRouter({
    'websocket':AllowedHostsOriginValidator(
        URLRouter([
            path('ws/<roomId>/',ChatRoomConsumer.as_asgi())
        ])
    )
})
