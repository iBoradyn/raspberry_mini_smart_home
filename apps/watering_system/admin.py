"""Watering system admin."""
# Django
from django.contrib import admin

# Local
from .models import Pump


@admin.register(Pump)
class PumpAdmin(admin.ModelAdmin):  # noqa: D101
    pass
