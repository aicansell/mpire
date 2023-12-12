from django.db import models

from authentication.models import User

class Message(models.Model):
    message = models.CharField(max_length=500)
    
    def __str__(self) -> str:
        return self.message

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    mark_read = models.BooleanField(default=False)
    
    def __str__(self) -> str:
        return f"{self.title} - {self.mark_read}"
