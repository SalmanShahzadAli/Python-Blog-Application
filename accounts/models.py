from django.contrib.auth.models import AbstractUser
from django.db import models

from django.contrib.auth.base_user import BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_approved', True)  # superuser is auto-approved
        return self.create_user(email, username, password, **extra_fields)
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    objects = CustomUserManager()
    # Admin approval workflow
    is_approved = models.BooleanField(
        default=False,
        help_text="Set to True by admin to allow the user to log in and use the site."
    )

    # Email is now the login field instead of username
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']  # still asked for at createsuperuser time

    def __str__(self):
        return self.email