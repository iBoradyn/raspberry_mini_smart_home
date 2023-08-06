"""Watering system views."""
# Django
from django.http import JsonResponse
from django.views import View

# Local
from .models import Pump
from .tasks import turn_on_pump_task
from .utils import turn_off_pump


class TurnOnPumpView(View):  # noqa: D101
    def post(self, *args, **kwargs):  # noqa: D102
        pump = Pump.objects.first()

        if pump.status == pump.PumpStatuses.ON:
            return JsonResponse(
                {
                    'message': 'Pump already working!',
                    'pump_status': pump.get_status_display(),
                },
                status=400
            )
        if pump.status == pump.PumpStatuses.TURNING_OFF:
            return JsonResponse(
                {
                    'message': 'Pump is turning off!',
                    'pump_status': pump.get_status_display(),
                },
                status=400
            )

        turn_on_pump_task.delay(pump.pk)

        return JsonResponse(
            {
                'message': 'Pump turned on.',
            },
            status=200
        )


class TurnOffPumpView(View):  # noqa: D101
    def post(self, *args, **kwargs):  # noqa: D102
        pump = Pump.objects.first()
        turn_off_pump(pump)

        return JsonResponse(
            {
                'message': 'Pump turned off.',
            },
            status=200
        )


class GetPumpStatus(View):  # noqa: D101
    def get(self, *args, **kwargs):  # noqa: D102
        pump_status = Pump.objects.first().get_status_display()

        return JsonResponse(
            {
                'pump_status': pump_status,
            },
            status=200
        )
