from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils import timezone

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, phone, full_name, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        
        # Extract user_type from extra_fields or default to 'student'
        user_type = extra_fields.pop('user_type', 'student')
        
        email = self.normalize_email(email)
        user = self.model(email=email, phone=phone, full_name=full_name, user_type=user_type, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('user_type', 'admin')  # Ensure superuser has the admin type
        return self.create_user(email, password, **extra_fields)



class CustomUser(AbstractBaseUser):
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)

    user_type = models.CharField(max_length=10, choices=[('admin', 'Admin'), ('student', 'Student')])

    full_name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone', 'full_name']

    def __str__(self):
        return self.email
