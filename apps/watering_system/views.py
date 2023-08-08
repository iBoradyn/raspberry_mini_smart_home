"""Watering system views."""
import json

# Django
from django.http import JsonResponse
from django.views import View
from django.views.generic import TemplateView
from django.utils.translation import gettext_lazy as _

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
                    'message': _('Pump already working!'),
                    'pump_status': pump.get_status_display(),
                },
                status=400
            )
        if pump.status == pump.PumpStatuses.TURNING_OFF:
            return JsonResponse(
                {
                    'message': _('Pump is turning off!'),
                    'pump_status': pump.get_status_display(),
                },
                status=400
            )

        turn_on_pump_task.delay(pump.pk)

        return JsonResponse(
            {
                'message': _('Pump turned on.'),
            },
            status=200
        )


class TurnOffPumpView(View):  # noqa: D101
    def post(self, *args, **kwargs):  # noqa: D102
        pump = Pump.objects.first()
        turn_off_pump(pump)

        return JsonResponse(
            {
                'message': _('Pump turned off.'),
            },
            status=200
        )


class GetPumpStatus(View):  # noqa: D101
    def get(self, *args, **kwargs):  # noqa: D102
        pump_status = Pump.objects.first().status

        return JsonResponse(
            {
                'pump_status': pump_status,
            },
            status=200
        )


class PumpControlTemplateView(TemplateView):
    template_name = 'watering_system/index.html'

    def get_context_data(self, **kwargs):  # noqa: D102
        context = super().get_context_data(**kwargs)

        pump_statuses = dict(
            zip(Pump.PumpStatuses.__members__.keys(), Pump.PumpStatuses.values),
        )
        context['pump_statuses'] = json.dumps(pump_statuses)

        pump_statuses_display = dict(Pump.PumpStatuses.choices)
        pump_statuses_display = {str(k): str(v) for k, v in pump_statuses_display.items()}
        context['pump_statuses_display'] = json.dumps(pump_statuses_display)

        return context
