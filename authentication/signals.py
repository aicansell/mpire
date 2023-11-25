from django.dispatch import receiver
from django.urls import reverse
from django.db.models.signals import post_save
from django.contrib.sites.shortcuts import get_current_site
from django_rest_passwordreset.signals import reset_password_token_created

from authentication.models import User, EmailConfirmationToken
from authentication.utils import send_email

@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    url = instance.request.build_absolute_uri(
        reverse('password_reset:reset-password-request')
        )
    
    data = {
        'name': reset_password_token.user.first_name + ' ' + reset_password_token.user.last_name,
        'link': f"{url}confirm/?token={reset_password_token.key}",
    }
    
    send_email(
        template_name="reset_password_email.txt",
        data=data,
        subject="Password reset",
        to=[reset_password_token.user.email]
    )


@receiver(post_save, sender=User)
def send_verification_email(sender, instance, created, **kwargs):
    if created:
        from .models import EmailConfirmationToken

        token = EmailConfirmationToken.objects.create(user=instance)
        token.save()

        verification_url = f"http://mpirebackend.eba-cnyr2zti.ap-south-1.elasticbeanstalk.com/verify/?token={token.id}"

        # Create the email content
        data = {
            'name': instance.first_name + ' ' + instance.last_name,
            'link': verification_url,
        }
        
        send_email(
            template_name="email_confirmation_mail.txt",
            data=data,
            subject="Email Verification",
            to=[instance.email]
        )
