from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, user_type, **extra_fields):
        email = self.normalize_email(email)

        user = self.model(email=email, user_type=user_type, **extra_fields)

        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, email, password,user_type, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser has to have is staff being True")
        
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser has to have is s uperuser being True")
        
        return self.create_user(email=email, password=password, user_type=user_type, **extra_fields)


class CustomUser(AbstractUser):
    reset_token = models.CharField(max_length=100, blank=True, null=True)
    reset_token_expires = models.DateTimeField(null=True, blank=True)
    phone = models.CharField(null=True, blank=True, max_length=15)

    image = models.ImageField(blank=True, null=True, upload_to='user_images')

    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    full_name = models.CharField(max_length=255)


    username = models.CharField(max_length=80, unique=False, blank=True, null=True)
    email = models.EmailField(max_length=80, unique=True)
    user_type = models.CharField(max_length=10, choices=[('admin', 'Admin'), ('client', 'Client')])

    objects = CustomUserManager()
    USERNAME_FIELD = "email"  # Set the email field as the unique identifier
    REQUIRED_FIELDS = ["user_type"]

    def __str__(self):
        return self.email


