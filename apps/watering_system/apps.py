"""Watering system apps."""
# Django
from django.apps import AppConfig


class WateringSystemConfig(AppConfig):  # noqa: D101
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.watering_system'
