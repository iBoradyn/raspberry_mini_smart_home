"""Door opener apps."""
# Django
from django.apps import AppConfig


class DoorOpenerConfig(AppConfig):  # noqa: D101
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.door_opener'
