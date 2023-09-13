"""Watering system views."""
# Standard Library
import json

# Django
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views import View
from django.views.generic import CreateView
from django.views.generic import DeleteView
from django.views.generic import ListView
from django.views.generic import TemplateView
from django.views.generic import UpdateView

# 3rd-party
from django_celery_beat.models import PeriodicTask

# Local
from .forms import ScheduleForm
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


class PumpControlTemplateView(TemplateView):  # noqa: D101
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


class SchedulesListView(ListView):  # noqa: D101
    template_name = 'watering_system/schedules/schedules_list.html'
    model = PeriodicTask

    def get_queryset(self):  # noqa: D102
        qr = super().get_queryset().order_by('-enabled', 'crontab__hour', 'crontab__minute')

        return qr.filter(task='apps.watering_system.tasks.turn_on_pump_task')


class ScheduleCreateView(CreateView):  # noqa: D101
    template_name = 'watering_system/schedules/create_schedule.html'
    form_class = ScheduleForm
    success_url = reverse_lazy('watering_system:schedules_list')


class ScheduleUpdateView(UpdateView):  # noqa: D101
    template_name = 'watering_system/schedules/update_schedule.html'
    model = PeriodicTask
    form_class = ScheduleForm
    success_url = reverse_lazy('watering_system:schedules_list')

    def get_form_kwargs(self):  # noqa: D102
        kwargs = super().get_form_kwargs()
        crontab = kwargs['instance'].crontab

        days = crontab.day_of_week

        kwargs['initial']['hour'] = crontab.hour
        kwargs['initial']['minute'] = crontab.minute
        kwargs['initial']['enabled'] = kwargs['instance'].enabled

        kwargs['initial']['day_of_week'] = list(range(7))
        if days != '*':
            kwargs['initial']['day_of_week'] = days.split(',')

        return kwargs


class ScheduleDeleteView(DeleteView):  # noqa: D101
    model = PeriodicTask
    success_url = reverse_lazy('watering_system:schedules_list')
