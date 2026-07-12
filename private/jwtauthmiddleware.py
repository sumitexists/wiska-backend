import urllib.parse
from channels.middleware import BaseMiddleware
from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from jwt import decode as jwt_decode
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from channels.db import database_sync_to_async

@database_sync_to_async
def get_user(validated_token):
    """Safely fetch the user from the database using the token payload"""
    try:
        user = get_user_model().objects.get(id=validated_token["user_id"])
        return user
    except get_user_model().DoesNotExist:
        return AnonymousUser()

class TokenAuthMiddleware(BaseMiddleware):
    """
    Custom Middleware that intercepts the WebSocket handshake, 
    extracts the JWT token from the query string (?token=...), 
    and authenticates the user.
    """
    async def __call__(self, scope, receive, send):
        # 1. Extract the query string from the WebSocket URL
        query_string = scope.get('query_string', b'').decode()
        query_params = urllib.parse.parse_qs(query_string)
        
        # 2. Grab the token from the query params
        token = query_params.get('token', [None])[0]

        if token:
            try:
                # 3. Verify the token is mathematically valid
                UntypedToken(token)
                
                # 4. Decode the payload to get the user_id
                decoded_data = jwt_decode(token, settings.SECRET_KEY, algorithms=["HS256"])
                
                # 5. Fetch the user and attach it to the scope
                scope['user'] = await get_user(decoded_data)
                
            except (InvalidToken, TokenError, Exception) as e:
                print(f"🚨 WebSocket Token Error: {e}")
                scope['user'] = AnonymousUser()
        else:
            print("🚨 WebSocket Connection Attempted without Token")
            scope['user'] = AnonymousUser()

        # Pass the scope down to the consumer
        return await super().__call__(scope, receive, send)