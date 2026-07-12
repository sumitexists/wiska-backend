from django.db import models

from accounts.models import AnonymousAlias

# Create your models here.


#Creating a Community model to represent the communities that users can create and join in the anonymous social media platform.
class Community(models.Model):
    class Meta:
        verbose_name_plural = "Communities"
        ordering = ['name']
    owner = models.ForeignKey(AnonymousAlias, on_delete=models.CASCADE, related_name='communities')
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    members = models.ManyToManyField(AnonymousAlias, related_name='joined_communities', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


#Creating a Post model to represent the posts that users can create within communities in the anonymous social media platform.  
class Post(models.Model):
    class Meta:
        verbose_name_plural = "Posts"
        ordering = ['-created_at']
    author = models.ForeignKey(AnonymousAlias, on_delete=models.CASCADE, related_name='post_author')
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    community = models.ForeignKey(Community, on_delete=models.CASCADE, related_name='post_community', blank=True, null=True)

    def __str__(self):
        return f'{self.title} by {self.author.username}'
    
#Creating a Comment model to represent the comments that users can create on posts in the anonymous social media platform.
class Comment(models.Model):
    class Meta:
        verbose_name_plural = "Comments"
        ordering = ['-created_at']
    
    author = models.ForeignKey(AnonymousAlias, on_delete=models.CASCADE, related_name='comment_author')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.author.username} on {self.post.title}'
    
#Creating a Like model to represent the likes that users can give to posts in the anonymous social media platform.
class Like(models.Model):
    class Meta:
        verbose_name_plural = "Likes"
        ordering = ['-liked_at']
    
    user = models.ForeignKey(AnonymousAlias, on_delete=models.CASCADE, related_name='like_user')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_liked')
    liked_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} liked {self.post.title}'
    
#Creating a model to list the following users of a community in the anonymous social media platform.
class Following(models.Model):
    class Meta:
        verbose_name_plural = "Following"
        ordering = ['-followed_at']
    
    user = models.ForeignKey(AnonymousAlias, on_delete=models.CASCADE, related_name='following_user')
    community = models.ForeignKey(Community, on_delete=models.CASCADE, related_name='community_followers')
    followed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} follows {self.community.name}'