from django.contrib import admin

from notifications.models import Notification, Message

admin.site.register(Notification)
admin.site.register(Message)
