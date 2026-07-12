import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from private.models import KnownContacts
from private.serializers import MessagesWebsocketSerializer
from django.db.models import Q

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.contact_id = self.scope['url_route']['kwargs']['contact_id']
        self.user = self.scope["user"]

        # 🚨 SECURITY GATEKEEPER 🚨
        is_authorized = await database_sync_to_async(
            KnownContacts.objects.filter(Q(user=self.user, contact_id=self.contact_id) | Q(user_id=self.contact_id, contact=self.user)).exists
        )()

        if not is_authorized:
            await self.close()
            print(self.user.get_username(), self.contact_id)
            return
        
        if self.user.id > int(self.contact_id):
            group_id=f"{self.user.id}_{self.contact_id}"
        else:
            group_id=f"{self.contact_id}_{self.user.id}"

        self.room_group_name = f"chat_{group_id}"
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        if hasattr(self, 'room_group_name'):
            await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        data['sender'] = self.user.id
        
        serializer = MessagesWebsocketSerializer(data=data, context={'user': self.user})
        
        if await database_sync_to_async(serializer.is_valid)():
            # Save to DB
            instance = await database_sync_to_async(serializer.save)()
            
            # Re-serialize the saved instance to include computed fields (is_sender, sender_details, etc.)
            output_serializer = MessagesWebsocketSerializer(instance, context={'user': self.user})
            output_data = await database_sync_to_async(lambda: output_serializer.data)()
            
            # BROADCAST: This sends the event to the group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message', 
                    'message': output_data # 🚨 This is a beautifully formatted Python Dictionary!
                }
            )
        else:
            print("Serializer Errors:", serializer.errors)

    # 🚨 ROUTING METHOD: Called by group_send for EVERY user in the room
    async def chat_message(self, event):
        # 1. Grab the dictionary that the Megaphone just shouted. 
        # We copy it so we can safely mutate it for this specific user.
        message_data = event['message'].copy() 
        
        # 2. THE ARCHITECT'S PUB/SUB FIX
        # We look at the 'sender' ID baked into the dictionary. 
        # If it matches the user connected to THIS SPECIFIC WebSocket instance, they are the sender.
        if message_data.get('sender') == self.user.id:
            message_data['is_sender'] = True
        else:
            message_data['is_sender'] = False
            
        # 3. Send the personalized data to the React frontend
        await self.send(text_data=json.dumps(message_data))