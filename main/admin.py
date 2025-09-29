from django.contrib import admin

# Register your models here.

from .models import Room, Topic, Message

admin.site.register(Room)   #register to see model in admin page
admin.site.register(Topic)
admin.site.register(Message)