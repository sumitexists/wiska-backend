from rest_framework.exceptions import NotFound
from django.http import HttpResponse


from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from accounts.models import AnonymousAlias, User
from accounts.serializers import AnonymousAliasSerializer, UserSerializer

#Created the viewsets so that admin can see the list of all users and also create new users. This view is only accessible to admin users.

def health_check(request):
    return HttpResponse("OK", status=200)

# ==========================================
# DOMAIN: CORE PROFILES (The Heavy Lifters)
# ==========================================


class UserViewset(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    

    
            

class AnonymousAliasView(generics.RetrieveAPIView):
    queryset = AnonymousAlias.objects.all()
    serializer_class = AnonymousAliasSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        user = self.request.user
        try:
            return AnonymousAlias.objects.get(user=user)
        except AnonymousAlias.DoesNotExist:
            raise NotFound("Anonymous alias not found for this user.")