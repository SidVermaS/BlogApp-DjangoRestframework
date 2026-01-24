import uuid
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from backend.core.base import BaseModel

class ProfileManager(BaseUserManager):
    def create_user(self, email, password = None, **extra_fields):
        if not email:
            raise ValueError("email is required")
        if not password:
            raise ValueError("password is required")
             
        email = self.normalize_email(email)
        profile = self.model(email = email, **extra_fields)
        profile.set_password(password)
        profile.full_clean()
        profile.save(using=self._db)
        return profile


class Profile(AbstractBaseUser, PermissionsMixin, BaseModel):
    class Status(models.TextChoices):
        ACTIVE = 'ACTIVE'
        BLOCKED = 'BLOCKED'

    email = models.EmailField(unique = True)
    name = models.CharField(max_length = 100)
    status = models.CharField(max_length = 10, choices = Status.choices, default = Status.ACTIVE, db_index = True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    objects = ProfileManager()

    class Meta:
        db_table = 'profile'

    def __str__(self):
        return self.email