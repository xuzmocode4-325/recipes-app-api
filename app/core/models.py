"""
Database models.
"""
from django.db import models 
from django.contrib.auth.models import (
    AbstractBaseUser, 
    BaseUserManager, 
    PermissionsMixin
)


class UserManager(BaseUserManager):
    """Class for creating a user manager"""

    def create_user(self, email, password=None, **kwargs):
        """Create, save and return a new user."""
        user = self.model(email=email, **kwargs)
        user.set_password(password)
        user.save(using=self._db)

        

class User(AbstractBaseUser, PermissionsMixin):
    """Model for custom definition of system user fields"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
