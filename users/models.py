from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from .managers import UserManager


class User(AbstractUser):
    class Role(models.IntegerChoices):
        Job_Seeker = 1
        Employer = 2
        Admin = 3

    username = None
    email = models.EmailField(_("email address"), unique=True)
    role = models.SmallIntegerField(choices=Role, default=Role.Job_Seeker)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email
