from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from authentication.models import User, EmailConfirmationToken

admin.site.site_header = _('Mpire')
admin.site.site_title = _('Admin')
admin.site.index_title = _('Mpire Portal')  

admin.site.register(User)
admin.site.register(EmailConfirmationToken)
