"""Project celery config."""
# Standard Library
import os

# 3rd-party
# 3rd-Party
from celery import Celery
from celery.signals import setup_logging

# Local
from .settings import env

# Setting up
broker_url = env.str('REDIS_URL')
result_backend = env.str('REDIS_URL')
# Configurations
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
# Celery
app = Celery(
    'project',
    broker=env.str('REDIS_URL'),
    backend=env.str('REDIS_URL'),
)
app.conf.result_backend = env.str('REDIS_URL')
app.config_from_object('django.conf:settings', namespace='CELERY')


# Logging
@setup_logging.connect
def config_loggers(*args, **kwargs):  # noqa: D103
    # Standard Library
    from logging.config import dictConfig

    # Django
    from django.conf import settings

    dictConfig(settings.LOGGING)


# Task Finder
app.autodiscover_tasks()
