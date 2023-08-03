"""Watering system views."""
# Django
from django.http import JsonResponse
from django.views import View

# 3rd-party
from gpiozero import OutputDevice

relay = OutputDevice(15, False)


class TurnOnPumpView(View):  # noqa: D101
    def post(self, *args, **kwargs):  # noqa: D102
        relay.on()

        return JsonResponse(
            {
              'pump_status': 'on',
            },
            status=200
        )


class TurnOffPumpView(View):  # noqa: D101
    def post(self, *args, **kwargs):  # noqa: D102
        relay.off()

        return JsonResponse(
            {
              'pump_status': 'off',
            },
            status=200
        )
