from django.urls import re_path
from private import consumers

websocket_urlpatterns = [
    # 🚨 THE RE-PATH 🚨
    # This exactly matches: ws://localhost:8000/private/messages/ws/chat/3/
    re_path(r"private/messages/ws/chat/(?P<contact_id>\d+)/$", consumers.ChatConsumer.as_asgi()),
]