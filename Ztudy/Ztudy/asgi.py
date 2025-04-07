import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import socket_service.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Ztudy.settings')
application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            socket_service.routing.websocket_urlpatterns
        )
    ),
})