"""Door opener admin."""
# Django
from django.contrib import admin

# Local
from .models import Motor


@admin.register(Motor)
class MotorAdmin(admin.ModelAdmin):  # noqa: D101
    pass
