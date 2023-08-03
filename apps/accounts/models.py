"""Accounts models."""
# Django
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):  # noqa: D101
    pass
