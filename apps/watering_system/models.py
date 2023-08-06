"""Watering system models."""
# Django
from django.db import models
from django.utils.translation import gettext_lazy as _


class Pump(models.Model):  # noqa: D101
    class PumpStatuses(models.TextChoices):  # noqa: D106
        ON = 'ON', _('Turned on')
        OFF = 'OFF', _('Turned off')
        TURNING_OFF = 'TURNING_OFF', _('Turning off')

    status = models.TextField(
        _('Status'),
        choices=PumpStatuses.choices,
        default=PumpStatuses.OFF,
    )

    pumping_time = models.IntegerField(_('Pumping time (s)'), default=60)

    class Meta:  # noqa: D106
        verbose_name = _('Pump')
        verbose_name_plural = _('Pumps')
