from authentication.utils import send_email
from authentication.models import User

def send_quote_email(requestquote, contact_me=None):
    data = {
        'request_user': requestquote.requestuser.get_full_name(),
        'product_name': requestquote.product.name,
        'message': requestquote.message
    }
    
    mails = []
        
    if not contact_me:
        admin_mails = User.objects.filter(user_type='admin').values_list('email', flat=True)
        mails.extend(admin_mails)
        mails.append(requestquote.product.created_by.email)
    else:
        mails.append(requestquote.product.created_by.email)

    send_email(
        template_name="request_quote_vendor_and_admin.txt",
        data=data,
        subject="New Request Quote",
        to=mails
    )
