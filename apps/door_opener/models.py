"""Door opener models."""
# Django
from django.db import models
from django.utils.translation import gettext_lazy as _


class Motor(models.Model):  # noqa: D101
    class MotorStatuses(models.TextChoices):  # noqa: D106
        LEFT_SPINNING = 'LEFT', _('Closing')
        RIGHT_SPINNING = 'RIGHT', _('Opening')
        NO_SPINNING = 'OFF', _('Turned off')
        TURNING_ON_SPINNING = 'TURNING_ON', _('Turning on')
        TURNING_OFF_SPINNING = 'TURNING_OFF', _('Turning off')

    class DoorStatuses(models.TextChoices):  # noqa: D106
        OPEN = 'OPEN', _('Open')
        CLOSED = 'CLOSED', _('Closed')
        OPENING = 'OPENING', _('Opening')
        CLOSING = 'CLOSING', _('Closing')

    status = models.TextField(
        _('Status'),
        choices=MotorStatuses.choices,
        default=MotorStatuses.NO_SPINNING,
    )

    door_status = models.TextField(
        _('Door status'),
        choices=DoorStatuses.choices,
        default=DoorStatuses.OPEN,
    )

    left_spinning_time = models.IntegerField(_('Left spinning time (s)'), default=60)
    right_spinning_time = models.IntegerField(_('Left spinning time (s)'), default=60)

    class Meta:  # noqa: D106
        verbose_name = _('Motor')
        verbose_name_plural = _('Motors')
