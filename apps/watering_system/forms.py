"""Watering system forms."""
# Django
from django import forms
from django.utils.translation import gettext_lazy as _

# 3rd-party
from django_celery_beat.models import CrontabSchedule
from django_celery_beat.models import PeriodicTask

# Project
from apps.core.utils import set_bootstrap_class
from apps.watering_system.models import Pump


class ScheduleForm(forms.ModelForm):  # noqa: D101
    DAYS = (
        (1, _('Monday')),
        (2, _('Tuesday')),
        (3, _('Wednesday')),
        (4, _('Thursday')),
        (5, _('Friday')),
        (6, _('Saturday')),
        (7, _('Sunday')),
    )

    hour = forms.IntegerField(max_value=23, min_value=0, initial=0, label=_('Hour'))
    minute = forms.IntegerField(max_value=59, min_value=0, initial=0, label=_('Minute'))
    day_of_week = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        choices=DAYS,
        label=_('Days'),
    )
    enabled = forms.BooleanField(initial=True, label=_('Enabled'), required=False)

    class Meta:  # noqa: D106
        model = PeriodicTask
        fields = [
            'hour',
            'minute',
            'day_of_week',
            'enabled',
            'name',
            'task',
            'crontab',
            'kwargs',
        ]

        widgets = {
            'name': forms.HiddenInput(),
            'task': forms.HiddenInput(),
            'crontab': forms.HiddenInput(),
            'kwargs': forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):  # noqa: D107
        super().__init__(*args, **kwargs)

        self.fields['name'].required = False
        self.fields['task'].required = False

        set_bootstrap_class(self.fields)

    def clean(self):  # noqa: D102
        cleaned_data = super().clean()

        hour = cleaned_data['hour']
        minute = cleaned_data['minute']
        days = ','.join(cleaned_data['day_of_week'])

        name = f'watering_system_{hour}:{minute}_{days}_'
        same_tasks = PeriodicTask.objects.filter(name__contains=name)

        task_number = 0
        if same_tasks:
            prev_task = same_tasks.latest('pk')
            prev_task_number = prev_task.name.split('_')[-1]
            task_number = int(prev_task_number) + 1

        cleaned_data['name'] = f'{name}{task_number}'
        cleaned_data['task'] = 'apps.watering_system.tasks.turn_on_pump_task'
        cleaned_data['crontab'], _ = CrontabSchedule.objects.get_or_create(
            minute=minute,
            hour=hour,
            day_of_week=days,
            timezone='Europe/Warsaw',
        )

        pump = Pump.objects.first()
        cleaned_data['kwargs'] = f'{{"pump_pk": {pump.pk}}}'

        return cleaned_data
