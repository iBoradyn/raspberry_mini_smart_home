"""Door opener models."""
# Django
from django.db import models
from django.utils.translation import gettext_lazy as _


class Motor(models.Model):  # noqa: D101
    class MotorStatuses(models.TextChoices):  # noqa: D106
        LEFT_SPINNING = 'LEFT', _('Left spinning')
        RIGHT_SPINNING = 'RIGHT', _('Right spinning')
        NO_SPINNING = 'OFF', _('Turned off')

    status = models.TextField(
        _('Status'),
        choices=MotorStatuses.choices,
        default=MotorStatuses.NO_SPINNING,
    )

    left_spinning_time = models.IntegerField(_('Left spinning time (s)'), default=60)
    right_spinning_time = models.IntegerField(_('Left spinning time (s)'), default=60)

    class Meta:  # noqa: D106
        verbose_name = _('Motor')
        verbose_name_plural = _('Motors')
