"""
ASGI config for wiska_core project.
"""
import os
import django

# 1. Set settings variable FIRST
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wiska_core.settings')

# 2. Boot up Django core BEFORE importing any routers or middleware
django.setup()

# 3. Safe to import core ASGI handler now
from django.core.asgi import get_asgi_application
django_asgi_app = get_asgi_application()

# 4. Safe to import Channels and custom app files now
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from private.jwtauthmiddleware import TokenAuthMiddleware
from private.routing import websocket_urlpatterns

# 5. Define your routing structure
application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AllowedHostsOriginValidator(
        TokenAuthMiddleware(
            URLRouter(
                websocket_urlpatterns
            )
        )
    )
})
