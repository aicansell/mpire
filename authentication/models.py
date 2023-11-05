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

    def create_superuser(self, email, password=None, **extra_fields):
        # Add a dummy 'username' argument with a default value
        username = extra_fields.pop('username', 'admin')

        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, username=username,**extra_fields)
    

class User(AbstractUser):
    ROLES = (
        ('customer', 'Customer'),
        ('vendor', 'Vendor'),
        ('admin', 'admin'),
        ('super_admin', 'Super Admin'),
    )
    
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=30, unique=False)
    user_type = models.CharField(max_length=50, choices=ROLES, default='customer')
    is_emailverified = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=20, unique=True)
    state = models.CharField(max_length=30)
    
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
