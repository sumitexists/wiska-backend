from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from accounts.models import AnonymousAlias

User = get_user_model()


@receiver(post_save, sender=User)
def create_anonymous_profile(sender, instance, created, **kwargs):
    if created:
        AnonymousAlias.objects.create(user=instance)
