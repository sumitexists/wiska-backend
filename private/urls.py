

from rest_framework import routers
from django.urls import path

from private import views
urlpatterns = [
    path('search-users/', views.SearchUserList.as_view(), name='search-users'),
]

router = routers.DefaultRouter()

router.register('messages', views.UserMessagesViewset)
router.register('contacts', views.KnownContactsListViewSet)

urlpatterns += router.urls