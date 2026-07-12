from django.contrib import admin

from private.models import Messages, KnownContacts

# Register your models here.
admin.site.register(Messages)
admin.site.register(KnownContacts)
    