from rest_framework import serializers

from accounts.models import AnonymousAlias, User


# ==========================================
# 1. USER SERIALIZER
# ==========================================
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
    


# ==========================================
# 2. ANONYMOUS ALIAS SERIALIZER
# ==========================================
class AnonymousAliasSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = AnonymousAlias
        fields = ['id', 'username']
        read_only_fields = ['user', 'username']



from djoser.serializers import UserCreatePasswordRetypeSerializer as BaseUserCreateSerializer
from django.contrib.auth import get_user_model

User = get_user_model()

class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        model = User
        fields = ('id', 'email', 'username', 'password', 'first_name', 'last_name')