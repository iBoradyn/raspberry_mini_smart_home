# Raspberry mini smart home
Api project for controlling electrical devices via raspberry pi


## Applications
### Watering system
Application managing a plant watering system.

### Door opener
An application that controls the rotation of the mini-motor that opens and closes the door on the slide gate.


## Required services
- PostrgeSQL
- Redis
- Gunicorn
- Daphne
- Celery
- Celery Beat


## Local project configuration
- Create postgresql database
- Create .env file based on .env.example
- `pip install -r requirements.txt` or `pip install -r requirements-dev.txt` for local development
- `python manage.py migrate`
- `python manage.py createsuperuser`
- `python manage.py collectstatic --noinput`
- Start redis on default port `6379`
  - `redis-server`
- Start Gunicorn on default port `8000`
  - `gunicorn --workers 3 project.wsgi:application`
- Start Daphne on port `8001`
  - `daphne -b 0.0.0.0 -p 8001 project.asgi:application`
- Start Celery worker
  - `celery -A project worker -l INFO`
- Start Celery Beat
  - `celery -A project beat -l INFO`
- Login to admin panel to create pump and motor objects and set timings.


## Project structure

```
raspberry_mini_smart_home
│   .env
│   requirements.txt
│   requirements-dev.txt
│   .gitignore
│   README.md
└───apps
│   └───accounts
│   └───core
│   └───door_opener
│   └───watering_system
└───locale
│   └───pl
└───project
│   │   asgi.py
│   │   celery_config.py
│   │   routing.py
│   │   settings.py
│   │   urls.py
│   │   wsgi.py
└───static
│   └───css
│   └───js
└───templates
    │ base.html
    └───core
    └───door_opener
    └───watering_system
```