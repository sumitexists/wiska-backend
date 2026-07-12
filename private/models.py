from django.conf import settings
from django.db import models

# Create your models here.


#Creating a Messages model to store the messages between users in the private messaging system. 
class Messages(models.Model):
    class Meta:
        verbose_name_plural = "Messages"
        ordering = ['-created_at']
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'Message from {self.sender.username} to {self.receiver.username} at {self.created_at}'

class FriendshipStatus(models.TextChoices):
    PENDING = 'PENDING', 'Pending'
    ACCEPTED = 'ACCEPTED', 'Accepted'
    REJECTED = 'REJECTED', 'Rejected'  

#Creating a model to represent list of known contacts.
class KnownContacts(models.Model):
    class Meta:
        verbose_name_plural = "Known Contacts"
        ordering = ['-added_at']
        # constraints = [
        #     models.UniqueConstraint(fields=['user', 'contact'], name='unique_user_contact')
        # ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='known_contacts')
    contact = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='contact_of')
    added_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=8, choices=FriendshipStatus.choices, default=FriendshipStatus.PENDING)

    def __str__(self):
        return f'{self.user.username} knows {self.contact.username}'