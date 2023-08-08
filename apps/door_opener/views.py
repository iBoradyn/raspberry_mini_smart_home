"""Door opener views."""
import json

# Django
from django.http import JsonResponse
from django.utils.translation import gettext_lazy as _
from django.views import View
from django.views.generic import TemplateView

# Local
from .models import Motor
from .tasks import spin_motor
from .utils import turn_off_motor


class CloseDoorView(View):  # noqa: D101
    def post(self, *args, **kwargs):  # noqa: D102
        motor = Motor.objects.first()

        if motor.status != motor.MotorStatuses.NO_SPINNING:
            return JsonResponse(
                {
                  'message': _('Motor already working!'),
                },
                status=400
            )

        spin_motor.delay(motor.pk, 'left')

        return JsonResponse(
            {
              'message': _('Door are closing.'),
            },
            status=200
        )


class OpenDoorView(View):  # noqa: D101
    def post(self, *args, **kwargs):  # noqa: D102
        motor = Motor.objects.first()

        if motor.status != motor.MotorStatuses.NO_SPINNING:
            return JsonResponse(
                {
                  'message': _('Motor already working!'),
                },
                status=400
            )

        spin_motor.delay(motor.pk, 'right')

        return JsonResponse(
            {
              'message': _('Door are opening.'),
            },
            status=200
        )


class TurnMotorOffView(View):  # noqa: D101
    def post(self, *args, **kwargs):  # noqa: D102
        motor = Motor.objects.first()
        turn_off_motor(motor)

        return JsonResponse(
            {
              'message': _('Motor stopped spinning.'),
            },
            status=200
        )


class GetDoorStatus(View):  # noqa: D101
    def get(self, *args, **kwargs):  # noqa: D102
        door_status = Motor.objects.first().door_status

        return JsonResponse(
            {
                'door_status': door_status,
            },
            status=200
        )


class MotorControlTemplateView(TemplateView):
    template_name = 'door_opener/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        door_statuses = dict(
            zip(Motor.DoorStatuses.__members__.keys(), Motor.DoorStatuses.values),
        )
        context['door_statuses'] = json.dumps(door_statuses)

        door_statuses_display = dict(Motor.DoorStatuses.choices)
        door_statuses_display = {str(k): str(v) for k, v in door_statuses_display.items()}
        context['door_statuses_display'] = json.dumps(door_statuses_display)

        return context
