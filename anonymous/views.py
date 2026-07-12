from rest_framework.response import Response
from rest_framework import filters, viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from django.utils import timezone

from .models import Comment, Community, Following, Like, Post
from .serializers import (CommentSerializer, CommunitySerializer,
                          FollowingSerializer, LikeSerializer, PostSerializer)
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page


# ==========================================
# 1. COMMUNITIES
# ==========================================
class CommunityViewSet(viewsets.ModelViewSet):
    queryset = Community.objects.select_related('owner').all().order_by('-created_at')
    serializer_class = CommunitySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    ordering = ['-created_at']
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'description']
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        sliced_queryset = queryset[:50]  # Limit to the first 50 communities
        serializer = self.get_serializer(sliced_queryset, many=True)
        return Response(serializer.data)
    
    def get_queryset(self):
        user_id = self.request.query_params.get('user_id')
        if user_id:
            return super().get_queryset().filter(community_followers__user_id=user_id)
        return super().get_queryset()

    def perform_update(self, serializer):
        # SECURITY: Only the mask that created the community can edit it
        if serializer.instance.owner != self.request.user.anonymous_user:
            raise PermissionDenied("You do not own this community.")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.owner != self.request.user.anonymous_user:
            raise PermissionDenied("You do not own this community.")
        instance.delete()
    
    def perform_create(self, serializer):
        # SECURITY: Automatically set the owner to the current user's mask
        serializer.save(owner=self.request.user.anonymous_user)


# ==========================================
# 2. POSTS (The Feed)
# ==========================================
class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'content', 'community__name']

    def get_queryset(self):
        qs = Post.objects.select_related('author','community').all().order_by('-created_at')
        
        # FILTER: Let the frontend ask for posts from ONE specific community
        # Example URL: /api/anonymous/posts/?community_id=5
        community_id = self.request.query_params.get('community_id')
        user_id = self.request.query_params.get('user_id')
        if community_id:
            qs = qs.filter(community_id=community_id)
        if user_id:
            qs = qs.filter(author_id = user_id)
            
        return qs
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        sliced_queryset = queryset[:50]  
        serializer = self.get_serializer(sliced_queryset, many=True)
        return Response(serializer.data)

    def perform_update(self, serializer):
        if serializer.instance.author != self.request.user.anonymous_user:
            raise PermissionDenied("You can only edit your own posts.")
        serializer.save(updated_at=timezone.now())

    def perform_destroy(self, instance):
        if instance.author != self.request.user.anonymous_user:
            raise PermissionDenied("You can only delete your own posts.")
        instance.delete()


# ==========================================
# 3. COMMENTS
# ==========================================
class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        qs = Comment.objects.select_related('author','post').all().order_by('created_at')
        
        # FILTER: Let the frontend fetch comments for ONE specific post
        # Example URL: /api/anonymous/comments/?post_id=12
        post_id = self.request.query_params.get('post_id')
        if post_id:
            qs = qs.filter(post_id=post_id)
            
        return qs.order_by("-created_at")

    def perform_update(self, serializer):
        if serializer.instance.author != self.request.user.anonymous_user:
            raise PermissionDenied("You can only edit your own comments.")
        serializer.save(updated_at=timezone.now())

    def perform_destroy(self, instance):
        if instance.author != self.request.user.anonymous_user:
            raise PermissionDenied("You can only delete your own comments.")
        instance.delete()


# ==========================================
# 4. LIKES & FOLLOWING (Interactions)
# ==========================================
class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.select_related('user', 'post').all()
    serializer_class = LikeSerializer
    permission_classes = [IsAuthenticated]
    
    http_method_names = ['get', 'post', 'delete', 'head', 'options']

    def perform_destroy(self, instance):
        if instance.user != self.request.user.anonymous_user:
            raise PermissionDenied("You can only remove your own likes.")
        instance.delete()
    
    def perform_create(self, serializer):
        user = Like.objects.filter(user=self.request.user.anonymous_user, post=serializer.validated_data['post']).first()
        if user:
            raise PermissionDenied("You have already liked this post.")
        serializer.save()


class FollowingViewSet(viewsets.ModelViewSet):
    queryset = Following.objects.select_related('user','community').all()
    serializer_class = FollowingSerializer
    permission_classes = [IsAuthenticated]
    
    http_method_names = ['get', 'post', 'delete', 'head', 'options']

    def perform_destroy(self, instance):
        if instance.user != self.request.user.anonymous_user:
            raise PermissionDenied("You can only unfollow communities you joined.")
        instance.delete()

    def perform_create(self, serializer):
        user = Following.objects.filter(user=self.request.user.anonymous_user, community=serializer.validated_data['community']).first()
        if user:
            raise PermissionDenied("You are already following this community.")
        serializer.save()
