from uuid import uuid4
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(
            email=email,
            password=password,
        )

        user.is_staff = True
        user.is_active = True
        user.is_superuser = True

        user.save(using=self._db)
        return user
    

class User(AbstractUser):
    ROLES = (
        ('customer', 'Customer'),
        ('vendor', 'Vendor'),
        ('admin', 'Admin'),
        ('super_admin', 'Super Admin'),
    )
    
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=30, unique=False, null=True, blank=True)
    user_type = models.CharField(max_length=50, choices=ROLES, default='customer')
    is_emailverified = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=20, unique=True, null=True, blank=True)
    state = models.CharField(max_length=30)
    first_time = models.BooleanField(default=False)
    profile_photo = models.FileField(upload_to='media/user/profile_photo', null=True, blank=True)
    
    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
        
    class Meta:
        db_table = 'auth_user'
        verbose_name = 'User'

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

class EmailConfirmationToken(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return f'{self.user.email} - {self.created_at}'

class VendorModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pancard = models.FileField(upload_to='media/vendor/pancard')
    gst = models.FileField(upload_to='media/vendor/gst')
    proof_of_registration = models.FileField(upload_to='media/vendor/proof_of_registration')
    approved = models.BooleanField(default=False)
    
    def __str__(self):
        return f'{self.user.first_name} - {self.approved}'
