from django.db import models
from django.utils.timezone import now

class Common(models.Model):
    created_at = models.DateTimeField(default=now)
    created_by = models.ForeignKey('authentication.User',
                                   on_delete=models.SET_NULL,
                                   null=True,
                                   related_name="%(app_label)s_%(class)s_created_by")
    
    updated_at = models.DateTimeField(default=now)
    updated_by = models.ForeignKey('authentication.User',
                                   on_delete=models.SET_NULL,
                                   null=True,
                                   related_name="%(app_label)s_%(class)s_updated_by")
    
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True)
    deleted_by = models.ForeignKey('authentication.User',
                                   on_delete=models.SET_NULL,
                                   null=True,
                                   related_name="%(app_label)s_%(class)s_deleted_by")
    
    class Meta:
        verbose_name = "Common"
        abstract = True
