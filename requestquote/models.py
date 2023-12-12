from django.db import models

from products.models import Product
from authentication.models import User

class RequestQuote(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    requestuser = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    mark_read = models.BooleanField(default=False)
    
    def __str__(self) -> str:
        return f"{self.product.name} - {self.requestuser.get_full_name()}"
