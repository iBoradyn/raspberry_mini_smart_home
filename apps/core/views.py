"""Core views."""
# Standard Library
import json

# Django
from django.views.generic import TemplateView

# Project
from apps.door_opener.models import Motor
from apps.watering_system.models import Pump


class IndexView(TemplateView):  # noqa: D101
    template_name = 'index.html'

    def get_context_data(self, **kwargs):  # noqa: D102
        context = super().get_context_data(**kwargs)

        pump_statuses = dict(Pump.PumpStatuses.choices)
        motor_statuses = dict(Motor.MotorStatuses.choices)

        pump_statuses = {str(k): str(v) for k, v in pump_statuses.items()}
        motor_statuses = {str(k): str(v) for k, v in motor_statuses.items()}

        context['pump_statuses'] = json.dumps(pump_statuses)
        context['motor_statuses'] = json.dumps(motor_statuses)

        return context
