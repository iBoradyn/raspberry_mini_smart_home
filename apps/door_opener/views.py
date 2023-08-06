"""Door opener views."""
# Django
from django.http import JsonResponse
from django.views import View

# Project
from apps.core.utils import flush_tasks_by_name

# Local
from .models import Motor
from .tasks import spin_motor
from .utils import turn_off_motor


class TurnMotorLeftSpinningView(View):  # noqa: D101
    def post(self, *args, **kwargs):  # noqa: D102
        motor = Motor.objects.first()

        if motor.status != motor.MotorStatuses.NO_SPINNING:
            return JsonResponse(
                {
                  'message': 'Motor already working!',
                },
                status=400
            )

        spin_motor.delay(motor.pk, 'left')

        return JsonResponse(
            {
              'message': 'Motor is spinning.',
            },
            status=200
        )


class TurnMotorRightSpinningView(View):  # noqa: D101
    def post(self, *args, **kwargs):  # noqa: D102
        motor = Motor.objects.first()

        if motor.status != motor.MotorStatuses.NO_SPINNING:
            return JsonResponse(
                {
                  'message': 'Motor already working!',
                },
                status=400
            )

        spin_motor.delay(motor.pk, 'right')

        return JsonResponse(
            {
              'message': 'Motor is spinning.',
            },
            status=200
        )


class TurnMotorOffView(View):  # noqa: D101
    def post(self, *args, **kwargs):  # noqa: D102
        motor = Motor.objects.first()
        turn_off_motor(motor)

        return JsonResponse(
            {
              'message': 'Motor stopped spinning.',
            },
            status=200
        )


class GetMotorStatus(View):  # noqa: D101
    def get(self, *args, **kwargs):  # noqa: D102
        motor_status = Motor.objects.first().get_status_display()

        return JsonResponse(
            {
                'motor_status': motor_status,
            },
            status=200
        )
