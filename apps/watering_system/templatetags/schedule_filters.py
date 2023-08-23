"""Watering system filters."""

# Django
from django import template
from django.utils.translation import gettext_lazy as _

register = template.Library()


DAYS_OF_WEEK = {
    0: _('Sunday'),
    1: _('Monday'),
    2: _('Tuesday'),
    3: _('Wednesday'),
    4: _('Thursday'),
    5: _('Friday'),
    6: _('Saturday'),
    7: _('Sunday'),
}


@register.filter
def get_time(schedule):  # noqa: D103
    hour = schedule.crontab.hour.zfill(2)
    minute = schedule.crontab.minute.zfill(2)
    return f'{hour}:{minute}'


@register.filter
def get_days(schedule):  # noqa: D103
    if schedule.crontab.day_of_week == '*':
        return list(DAYS_OF_WEEK.values())[1:]

    days = schedule.crontab.day_of_week.split(',')
    return [DAYS_OF_WEEK[int(day_number)] for day_number in days]
