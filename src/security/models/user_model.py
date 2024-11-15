"""
Models for the core app.
"""

from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.db import models

from core.management.commands.base_model import BaseModel
from core.management.commands.custom_user_manager import CustomUserManager


class User(AbstractUser, BaseModel, PermissionsMixin):
    """
    Class User model
    """

    status = models.CharField(max_length=15, null=False, default="New")
    email = models.EmailField(blank=True, unique=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    def __str__(self):
        return self.username

    class Meta:
        db_table = "user"
        ordering = ["created_at"]
