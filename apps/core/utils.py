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


def set_bootstrap_class(fields):  # noqa: D101
    """Set Bootstrap classes for specific fields."""
    classes_dict = {
        'CharField': {
            'field': 'form-control mb-4',
            'label': '',
        },
        'IntegerField': {
            'field': 'form-control mb-4',
            'label': '',
        },
        'DecimalField': {
            'field': 'form-control mb-4',
            'label': '',
        },
        'EmailField': {
            'field': 'form-control mb-4',
            'label': '',
        },
        'ChoiceField': {
            'field': 'form-control mb-4',
            'label': '',
        },
        'TypedChoiceField': {
            'field': 'form-control mb-4',
            'label': '',
        },
        'PasswordField': {
            'field': 'form-control mb-4',
            'label': '',
        },
        'SetPasswordField': {
            'field': 'form-control mb-4',
            'label': '',
        },
        'BooleanField': {
            'field': 'form-check-input',
            'label': '',
        },
        'ModelChoiceField': {
            'field': 'form-control mb-4',
            'label': '',
        },
        'ModelMultipleChoiceField': {
            'field': 'form-control select-200 mb-4',
            'label': '',
        },
        'MultipleChoiceField': {
            'field': '',
            'label': '',
        },
        'FileField': {
            'field': '',
            'label': '',
        },
        'DateField': {
            'field': 'form-control custom-datepicker mb-4',
            'label': '',
        },
        'DateTimeField': {
            'field': 'form-control custom-timepicker mb-4',
            'label': '',
        },
        'ImageField': {
            'field': '',
            'label': '',
        },
        'IconFormField': {
            'field': '',
            'label': '',
        },
        'PointField': {
            'field': '',
            'label': '',
        },
        'RegexField': {
            'field': 'form-control mb-4',
            'label': '',
        },
        'UsernameField': {
            'field': 'form-control mb-4',
            'label': '',
        },
    }
    for _, field in fields.items():
        try:
            field.widget.attrs.update(
                {
                    'class': classes_dict[field.__class__.__name__]['field'],
                    'placeholder': field.label,
                },
            )
        except KeyError:
            pass
