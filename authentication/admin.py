from django.contrib import admin

from authentication.models import User, EmailConfirmationToken

admin.site.register(User)
admin.site.register(EmailConfirmationToken)
