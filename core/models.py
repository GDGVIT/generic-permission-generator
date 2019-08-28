import uuid

from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import PermissionsMixin

class UserManager(BaseUserManager):
    def create_user(self, email, password, *args, **kwargs):
        if not email:
            raise ValueError(_("Email address must be provided"))
        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, *args, **kwargs):
        user = self.create_user(email=email, password=password)
        user.is_admin = True
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(verbose_name=_("Email Address"), unique=True)
    first_name = models.CharField(verbose_name="First name", max_length=255, blank=True)
    last_name = models.CharField(max_length=255, blank=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    jwt_secret = models.UUIDField(default=uuid.uuid4)
    date_joined = models.DateTimeField(verbose_name=_("Created on"), auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = "email"

    def __str__(self):
        return self.email

    @property
    def is_staff(self):
        return self.is_admin

    @property
    def is_superuser(self):
        return self.is_admin

    def get_full_name(self):
        return "{self.first_name} {self.last_name}"

    def get_first_name(self):
        return self.first_name

    def get_email(self):
        return self.email

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


def jwt_get_secret_key(user_model):
    return user_model.jwt_secret
