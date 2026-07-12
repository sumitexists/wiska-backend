from rest_framework import serializers
from django.db.models import Q
from private.models import (KnownContacts, Messages)
from accounts.models import User
from accounts.serializers import UserSerializer

# ==========================================
# 1. Messages Serializer
# ==========================================
class MessagesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Messages
        fields = ['id','sender', 'receiver', 'content', 'created_at']
        read_only_fields = ['id','sender', 'created_at' ]

    def get_is_sender(self, obj):
        request = self.context.get('request')
        if hasattr(request, 'user'):
            return obj.sender_id == request.user.id
        return False
    
    def validate_content (self,value):
        if len(value) > 500:
            raise serializers.ValidationError("Message must be under 500 character")
        return value

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['sender'] = request.user
        return super().create(validated_data)

# ==========================================
# 2. Known Contact Serializer
# ==========================================
class KnownContactSerializer(serializers.ModelSerializer):
    contact_details = serializers.SerializerMethodField()
    class Meta:
        model = KnownContacts
        fields = ['id','user', 'contact', 'contact_details']
        read_only_fields = ['id','user', 'contact_details']

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['user'] = request.user
        
        return super().create(validated_data)
    
    def get_contact_details(self, obj):
        request_user = self.context['request'].user
        if obj.user == request_user:
            friend = obj.contact
        else:
            friend = obj.user
            
        return UserSerializer(friend).data


    # ==========================================
# 3. MessagesWebsocket Serializer
# ==========================================
class MessagesWebsocketSerializer(serializers.ModelSerializer):

    class Meta:
        model = Messages
        fields = ['id','sender', 'receiver', 'content', 'created_at']
        read_only_fields = ['id','sender', 'created_at' ]


    
    def validate_content (self,value):
        if len(value) > 500:
            raise serializers.ValidationError("Message must be under 500 character")
        return value

    def create(self, validated_data):
        user = self.context.get('user')
        validated_data['sender'] = user
        return super().create(validated_data)


class SearchUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', "first_name", "last_name"]
        read_only_fields = ['id', 'username', "first_name", "last_name"]
