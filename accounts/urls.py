from rest_framework.routers import DefaultRouter
from django.urls import path

from accounts import views

router = DefaultRouter()
router.register('users', views.UserViewset)
urlpatterns = [
    path('anonymousUser/', views.AnonymousAliasView.as_view(), name='anonymous-alias'),
    path('health-check/', views.health_check, name='health-check')
]

urlpatterns += router.urls