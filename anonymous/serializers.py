from rest_framework import serializers
from anonymous.models import (Comment, Community, Following, Like, Post)


# ==========================================
# 1. COMMUNITY SERIALIZER
# ==========================================
class CommunitySerializer(serializers.ModelSerializer):
    number_of_members = serializers.IntegerField(source='community_followers.count', read_only=True)
    number_of_posts = serializers.IntegerField(source='post_community.count', read_only=True)
    owner_username = serializers.CharField(source='owner.username', read_only=True)
    is_member = serializers.SerializerMethodField()
    following_id = serializers.SerializerMethodField()

    class Meta:
        model = Community
        fields = ['id', 'name', 'owner', 'description', 'created_at', 'number_of_members', 'number_of_posts','owner_username', 'is_member', 'following_id']
        read_only_fields = ['id', 'owner', 'created_at', 'is_owner', 'owner_username', 'is_member', 'following_id']

    def validate_name(self, value):
        if len(value) > 30:
            raise serializers.ValidationError("Name cannot exceed 30 characters.")
        return value
    def validate_description(self, value):
        if len(value) > 200:
            raise serializers.ValidationError("Description cannot exceed 200 characters.")
        return value

    def get_is_member(self, obj):
        request = self.context.get("request")
        if request and hasattr(request, 'user') and request.user.is_authenticated:
            # Check if the user is a member of the community
            return obj.community_followers.filter(user=request.user.anonymous_user).exists()
        return False

    def get_following_id(self, obj):
        request = self.context.get("request")
        if request and hasattr(request, 'user') and request.user.is_authenticated:
            following = obj.community_followers.filter(user=request.user.anonymous_user).first()
            return following.id if following else None
        return None
    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['owner'] = request.user.anonymous_user
        return super().create(validated_data)


# ==========================================
# 2. POST SERIALIZER
# ==========================================
class PostSerializer(serializers.ModelSerializer):
    likes = serializers.IntegerField(source='post_liked.count', read_only=True)
    number_of_comments = serializers.IntegerField(source='post_comments.count', read_only=True)
    author_username = serializers.CharField(source='author.username', read_only=True)
    community_name = serializers.CharField(source='community.name', read_only=True)
    is_liked = serializers.SerializerMethodField()
    like_id = serializers.SerializerMethodField()
    class Meta:
        model = Post
        fields = ['id', 'author', 'title', 'content', 'created_at', 'likes', 'number_of_comments', 'author_username', 'community_name', 'is_liked', 'like_id', 'community']
        read_only_fields = ['id', 'author', 'created_at']

    def validate_title(self, value):
        if len(value) > 100:
            raise serializers.ValidationError("Title cannot exceed 100 characters.")
        return value

    def validate_content(self, value):
        if len(value) > 500:
            raise serializers.ValidationError("Content cannot exceed 500 characters.")
        return value

    def get_like_id(self, obj):
        request = self.context.get('request')
        if request and hasattr(request, 'user') and request.user.is_authenticated:
            like = Like.objects.filter(user=request.user.anonymous_user, post=obj).first()
            return like.id if like else None
        return None
    
    def get_is_author(self, obj):
        request = self.context.get('request')
        if request and hasattr(request, 'user') and request.user.is_authenticated:
            return obj.author == request.user.anonymous_user
        return False
    def get_is_liked(self, obj):
        request = self.context.get('request')
        if request and hasattr(request, 'user') and request.user.is_authenticated:
            return Like.objects.filter(user=request.user.anonymous_user, post=obj).exists()
        return False

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['author'] = request.user.anonymous_user
        return super().create(validated_data)


# ==========================================
# 3. COMMENT SERIALIZER
# ==========================================
class CommentSerializer(serializers.ModelSerializer):
    author_username = serializers.CharField(source='author.username' , read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'author', 'post', 'content', 'created_at', "author_username"]
    
        read_only_fields = ['id', 'author', 'created_at']


    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['author'] = request.user.anonymous_user
        return super().create(validated_data)


# ==========================================
# 4. LIKE SERIALIZER
# ==========================================
class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['id', 'user', 'post', 'liked_at']
        read_only_fields = ['id', 'user', 'liked_at']
    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['user'] = request.user.anonymous_user
        return super().create(validated_data)
    def validate_user(self, value):
        request = self.context.get('request')
        body = self.initial_data
        if request and hasattr(request, 'user') and request.user.is_authenticated:
            if value != request.user.anonymous_user:
                raise serializers.ValidationError("You can only like a post as yourself.")
# ==========================================
# 5. FOLLOWING SERIALIZER
# ==========================================
class FollowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Following
        fields = ['id', 'user', 'community', 'followed_at']
        read_only_fields = ['id', 'user', 'followed_at']

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['user'] = request.user.anonymous_user
        return super().create(validated_data)
