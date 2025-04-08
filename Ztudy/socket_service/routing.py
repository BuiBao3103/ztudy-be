from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'chat/(?P<code_invite>[\w-]+)/$', consumers.ChatConsumer.as_asgi()),
    re_path(r'online/$', consumers.OnlineStatusConsumer.as_asgi()),

    re_path(r'ws/chat/(?P<code_invite>[\w-]+)/$', consumers.ChatConsumer.as_asgi()),
    re_path(r'ws/online/$', consumers.OnlineStatusConsumer.as_asgi()),
]
