"""Project settings."""
# Standard Library
import os
from pathlib import Path

# Django
from django.utils.translation import gettext_lazy as _

# 3rd-party
import environ

BASE_DIR = Path(__file__).resolve().parent.parent

SITE_ID = 1

env = environ.Env(DEBUG=(bool, False))
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

if env.bool('MOCK_PINS', True):
    # 3rd-party
    from gpiozero import Device
    from gpiozero.pins.mock import MockFactory

    Device.pin_factory = MockFactory()

DEBUG = env.bool('DEBUG', False)
SECRET_KEY = env.str('SECRET_KEY', 'S3cR3tK3y')

ROOT_URLCONF = 'project.urls'
WSGI_APPLICATION = 'project.wsgi.application'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': env.str('DATABASE_NAME', ''),
        'USER': env.str('DATABASE_USER', ''),
        'PASSWORD': env.str('DATABASE_PASS', ''),
        'HOST': env.str('DATABASE_HOST', ''),
        'PORT': env.str('DATABASE_PORT', ''),
    }
}

# Installed Apps
INSTALLED_APPS = [
    'daphne',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # local
    'apps.core.apps.CoreConfig',
    'apps.accounts.apps.AccountsConfig',
    'apps.watering_system.apps.WateringSystemConfig',
    'apps.door_opener.apps.DoorOpenerConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# Debug Settings
if DEBUG:
    ALLOWED_HOSTS = ['*']
    CSRF_TRUSTED_ORIGINS = [
        'http://0.0.0.0:8000',
        'http://127.0.0.1:8000',
        f'https://{env.str("DOMAIN", "")}',
    ] + env.list('CSRF_MORE_ORIGINS', default=[])
else:
    ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=[])
    CSRF_TRUSTED_ORIGINS = [
                               f'https://{env.str("DOMAIN", "")}',
                           ] + env.list('CSRF_MORE_ORIGINS', default=[])

AUTH_USER_MODEL = 'accounts.CustomUser'

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
LANGUAGE_CODE = 'en-us'
LANGUAGES = [
    ('pl', _('Polish')),
    ('en', _('English')),
]

TIME_ZONE = 'Europe/Warsaw'
USE_I18N = True
USE_TZ = True

# Static
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'apps_static/')
# Media
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

# Email
EMAIL_BACKEND = env.str('EMAIL_BACKEND', '')
DEFAULT_FROM_EMAIL = env.str('DEFAULT_FROM_EMAIL', '')
EMAIL_HOST = env.str('EMAIL_HOST', '')
EMAIL_USE_TLS = env.bool('EMAIL_USE_TLS', '')
EMAIL_USE_SSL = env.bool('EMAIL_USE_SSL', '')
EMAIL_PORT = env.str('EMAIL_PORT', '')
EMAIL_HOST_USER = env.str('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = env.str('EMAIL_HOST_PASSWORD', '')

# Celery
CELERY = {
    'BROKER_URL': env.str('REDIS_URL'),
    'RESULT_BACKEND': env.str('REDIS_URL'),
    'TASK_SERIALIZER': 'json',
    'RESULT_SERIALIZER': 'json',
    'ACCEPT_CONTENT': ['json'],
    'TIMEZONE': 'Europe/Warsaw',
    'TASK_TRACK_STARTED': True,
    'TASK_RESULT_EXPIRES': 10000,
}
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'

# Channels
ASGI_APPLICATION = "project.asgi.application"
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("127.0.0.1", 6379)],
        },
    },
}
