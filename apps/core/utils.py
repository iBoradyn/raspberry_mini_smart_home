"""Core utils."""
# Project
from project.celery_config import app


def flush_tasks_by_name(module: str, name: str):  # noqa: D103
    i = app.control.inspect()
    task_name = f'{module}.{name}'

    scheduled = list(i.scheduled().values())[0]
    active = list(i.active().values())[0]
    reserved = list(i.reserved().values())[0]

    all_tasks = scheduled + active + reserved
    all_striped = [
        {
            'id': task['id'],
            'name': task['name'],
        } for task in all_tasks if task['name'] == task_name
    ]

    for task in all_striped:
        app.control.revoke(task['id'], terminate=True)
