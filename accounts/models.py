from django.contrib.auth.models import AbstractUser
from django.db import models

from accounts.utils import generate_anonymous_username

# Create your models here

class User(AbstractUser):
    #adding additional fields to default User model
    email = models.EmailField(unique=True) #overriding the default email field to make it unique
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    def __str__(self):
        return self.username




#Defining an AnonymousAlias model to differentiate and protecting from leaking actual data of the user .

class AnonymousAlias(models.Model):
    class Meta:
        verbose_name_plural = "Anonymous Aliases"
    user = models.OneToOneField(User, on_delete=models.CASCADE , related_name='anonymous_user')
    username = models.CharField(max_length = 64, unique = True, editable = False)

    #Defining a save method to generate a random username for the anonymous user and ensuring its uniqueness before saving the model instance.
    def save(self, *args, **kwargs):
        if not self.username:
            self.username = generate_anonymous_username()
        while AnonymousAlias.objects.filter(username=self.username).exists():
            if self.user.anonymous_user.username :
                break
            self.username = generate_anonymous_username()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} is anonymous as {self.username}"
