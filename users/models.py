from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.db.models import signals
from django.dispatch import receiver
from shop.models import UserCart

from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import ugettext_lazy as _


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):

    CUSTOMER = "customer"
    MANAGER = "manager"

    ROLE_CHOICES = [
        (CUSTOMER, 'клиент'),
        (MANAGER, 'менеджер'),

    ]
    role = models.TextField(
        choices=ROLE_CHOICES,
        default=CUSTOMER,
    )
    username = None
    email = models.EmailField(_('email address'), unique=True)
    full_name = models.CharField("ФИО", max_length=250)
    delivery_address = models.TextField("адресс", max_length=10000, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    username = None
    objects = CustomUserManager()


@receiver(signals.post_save, sender=User)
def create_cart(sender, instance, **kwargs):
    if len(UserCart.objects.filter(owner=instance)) == 0:
        UserCart.objects.create(owner=instance)
