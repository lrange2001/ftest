from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter

from django.urls import re_path
from server.websocket.terminal import SSHConsumer

application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(
        URLRouter([
            re_path(r'^server/terminal/(?P<hostname>.*)/', SSHConsumer.as_asgi()),
        ])
    ),
})