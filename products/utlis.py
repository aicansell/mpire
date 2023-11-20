from django.db.models import Q

from products.models import Product
from authentication.models import User
from authentication.utils import send_email


def Checking_Product(product_name, user):
    if not Product.objects.filter(name__icontains=product_name).exists():
        data = {
        'product_name': product_name,
        'name': user.first_name,
        'email': user.email,
        }
        
        admin_emails = User.objects.filter(user_type='admin').values_list('email', flat=True)
        
        
        send_email(
            template_name="product_not_found.txt",
            data=data,
            subject="Product Not Found",
            to= admin_emails,
        )
