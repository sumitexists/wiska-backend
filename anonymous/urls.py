from rest_framework.routers import DefaultRouter

from anonymous import views

#Using a DefaultRouter to automatically generate the URL patterns for the Viewsets.

#Defining router
router = DefaultRouter()

#Registering the Viewsets with the router to generate the URL patterns for the Community and Post endpoints.    
router.register('community', views.CommunityViewSet)
router.register('posts', views.PostViewSet, basename='posts')
router.register('likes', views.LikeViewSet)
router.register('comments', views.CommentViewSet, basename='comments')
router.register('following', views.FollowingViewSet)

#URL that is going to be used.
urlpatterns = router.urls