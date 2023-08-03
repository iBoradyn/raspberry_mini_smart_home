"""Door opener views."""
# Django
from django.http import JsonResponse
from django.views import View

# 3rd-party
from gpiozero import OutputDevice

relayLeft = OutputDevice(17, False)
relayRight = OutputDevice(22, False)


class TurnMotorLeftSpinningView(View):  # noqa: D101
    def post(self, *args, **kwargs):  # noqa: D102
        relayLeft.on()
        relayRight.off()

        return JsonResponse(
            {
              'motor_status': 'left_spinning',
            },
            status=200
        )


class TurnMotorRightSpinningView(View):  # noqa: D101
    def post(self, *args, **kwargs):  # noqa: D102
        relayLeft.off()
        relayRight.on()

        return JsonResponse(
            {
              'motor_status': 'right_spinning',
            },
            status=200
        )


class TurnMotorOffView(View):  # noqa: D101
    def post(self, *args, **kwargs):  # noqa: D102
        relayLeft.off()
        relayRight.off()

        return JsonResponse(
            {
              'motor_status': 'off',
            },
            status=200
        )
