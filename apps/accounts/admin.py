"""Accounts admin."""
# Django
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# Local
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):  # noqa: D101
    pass
