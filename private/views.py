from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from django.db.models import Q
from django.utils import timezone
from private.models import (Messages, KnownContacts)
from private.serializers import (MessagesSerializer, KnownContactSerializer, SearchUserSerializer)
from accounts.models import User
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import filters


#=============================================
# 1. UserMessagesViewset: A viewset to handle CRUD operations for messages between users.
#=============================================
class UserMessagesViewset(viewsets.ModelViewSet):
    queryset = Messages.objects.select_related('sender','receiver').all()
    serializer_class = MessagesSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        contact_id = self.request.query_params.get('contact_id')
        if not contact_id:
            return super().get_queryset().none()
        
        contact_id = int(contact_id)
        contact_record = KnownContacts.objects.filter(Q(user=self.request.user, contact_id=contact_id) | Q(user_id=contact_id, contact=self.request.user)).exists()
        if not contact_record:
            raise PermissionDenied("You are not allowed to view messages with this contact.")

        return super().get_queryset().filter(
            Q(sender=self.request.user, receiver_id=contact_id) | 
            Q(sender_id=contact_id, receiver=self.request.user)
            ).order_by('created_at')

    def perform_update(self, serializer):
        if serializer.instance.sender != self.request.user:
            raise PermissionDenied("You cannot edit a message someone else sent you.")
        serializer.save(updated_at=timezone.now())
    def perform_destroy(self, instance):
        if instance.sender != self.request.user:
            raise PermissionDenied("You cannot delete a message someone else sent you.")
        instance.delete()
    def perform_create(self, serializer):
        contact_id = self.request.data.get('receiver')
        if not contact_id:
            raise PermissionDenied("Receiver is required.")
        
        contact_record = KnownContacts.objects.filter(Q(user=self.request.user, contact_id=contact_id) | Q(user_id=contact_id, contact=self.request.user)).exists()
        if not contact_record:
            raise PermissionDenied("You can only send messages to known contacts.")
        
        serializer.save(sender=self.request.user, created_at=timezone.now(), updated_at=timezone.now())

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
    
    # 2. Serialize the data into a flat list of items
        serializer = self.get_serializer(queryset, many=True)

        contact_id = self.request.query_params.get('contact_id')
        if not contact_id:
            return Response({"error": "contact_id is required."}, status=400)
        contact = User.objects.filter(pk=contact_id).first().username
    
    # 3. Construct your custom response payload structure
        custom_response_payload = {       # Custom count key
        'contact': contact,   # Any custom data you want
        'results': serializer.data            # Your actual list of records
        }
    
    # 4. Return the dictionary wrapped in a DRF Response
        return Response(custom_response_payload)



#=============================================
# 2. KnownContactsListViewSet: A viewset to manage the list of known contacts for each user.
#=============================================
class KnownContactsListViewSet(viewsets.ModelViewSet):
    queryset = KnownContacts.objects.select_related('contact', 'user').all()
    serializer_class = KnownContactSerializer
    permission_classes = [IsAuthenticated]
    
    http_method_names = ['get', 'post', 'delete', 'head', 'options']

    def get_queryset(self):
        qs = super().get_queryset()
        if not self.request.user.is_staff:   
            return qs.filter(Q(user=self.request.user, status="ACCEPTED")|Q(contact=self.request.user, status="ACCEPTED")).order_by('added_at')
        return qs
    
    def perform_create(self, serializer):
        qs = super().get_queryset()
        contact_record = qs.filter(Q(user=self.request.user, contact_id=serializer.validated_data['contact']) | Q(user_id=serializer.validated_data['contact'], contact=self.request.user.id)).exists()
        if contact_record:
            raise PermissionDenied("This contact already exists.")
        serializer.save()

    @action(detail=False, methods=['post'], url_path='deleteContact', url_name='delete-contact')
    def delete_contact(self, request):
        qs = super().get_queryset()
        contact = request.data.get('contact')
        if not contact:
            return Response({"error": "contact is required."}, status=400)
        contact_record = qs.filter(Q(user=request.user, pk=contact) | Q(pk=contact, contact=request.user)).first()
        print(contact_record)
        if contact_record:
            contact_record.delete()
            return Response({"success": "Contact deleted successfully."}, status=200)
        return Response({"error": "Contact not found."}, status=404)
    

    @action(detail=False, methods=['get','post'], url_path='updateStatus', url_name='update-status')
    def update_status(self,request):
        qs = super().get_queryset()
        contact = request.data.get('contact')
        new_status = request.data.get('status')
        if not contact or not new_status:
            return Response({"error": "Both contact_id and status are required."}, status=400)
        contact_record = qs.filter(contact=request.user, pk=contact).first()
        if not contact_record:
            return Response({"error": "Contact not found."}, status=404)
        if new_status == "ACCEPTED":
            contact_record.status = new_status
            contact_record.save()
            return Response({"success": "Contact status updated successfully."}, status=200)
        elif new_status == "REJECTED":
            contact_record.delete()
            return Response({"success": "Contact rejected and deleted successfully."}, status=200)  

    @action(detail=False, methods=['get'], url_path='pendingRequests', url_name='pending-requests')
    def pending_requests(self, request):
        qs = super().get_queryset()
        pending_contacts = qs.filter(contact=request.user, status="PENDING").order_by('added_at')
        serializer = self.get_serializer(pending_contacts, many=True)
        return Response(serializer.data)     


class SearchUserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = SearchUserSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['username', 'email', 'first_name', 'last_name']

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        known_contact_ids = KnownContacts.objects.filter(user=user).values_list('contact_id', flat=True)
        known_user_ids = KnownContacts.objects.filter(contact=user).values_list('user_id', flat=True)
        all_known_ids = set(known_contact_ids) | set(known_user_ids)
        queryset = queryset.exclude(id=user.id).exclude(id__in=all_known_ids)
        return queryset
    def list(self, request, *args, **kwargs):
        queryset=self.get_queryset()
        serach_filter = self.filter_queryset(queryset)
        sliced_queryset = serach_filter[:20]
        serializer = self.get_serializer(sliced_queryset, many=True)
        return Response(serializer.data)
