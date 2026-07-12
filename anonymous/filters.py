import django_filters

from anonymous.models import Community, Post


class CommunityFilter(django_filters.FilterSet):
    class Meta:
        model = Community
        fields = {
                    'name': ['icontains'],
                    'owner__username': ['icontains']
                }
        

class PostFilter(django_filters.FilterSet):
    class Meta:
        model = Post
        fields = {
                    'title': ['icontains'],
                    'author__username': ['icontains'],
                    'content': ['icontains']
                }