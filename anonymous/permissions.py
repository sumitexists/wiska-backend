from rest_framework.permissions import BasePermission


class IsOwnerOrAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user or request.user.is_staff
    

class IsAuthorOrCommunityOwnerOrAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated
    def has_object_permission(self, request, view, obj):
        return obj.author == request.user or obj.community.owner == request.user or request.user.is_staff