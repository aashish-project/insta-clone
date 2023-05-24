from django.contrib import admin

# Register your models here.
from direct_message.models import Message

admin.site.register(Message)