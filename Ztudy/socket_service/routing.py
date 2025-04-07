from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    # Hỗ trợ URL có hoặc không có dấu `/`
    re_path(r'^/*ws/chat/(?P<code_invite>[\w-]+)/$', consumers.ChatConsumer.as_asgi()),
    re_path(r'^/*ws/online/$', consumers.OnlineStatusConsumer.as_asgi()),
]
