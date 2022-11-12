import os

from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
import user_home.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'messageapp.settings')

application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket':AuthMiddlewareStack(
        URLRouter(
            user_home.routing.websocket_urlpatterns
        )
    )
})
