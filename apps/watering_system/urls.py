"""Watering system urls."""
# Django
from django.contrib.auth.decorators import login_required
from django.urls import path

# Local
from .views import GetPumpStatus
from .views import PumpControlTemplateView
from .views import ScheduleCreateView
from .views import ScheduleDeleteView
from .views import SchedulesListView
from .views import ScheduleUpdateView
from .views import TurnOffPumpView
from .views import TurnOnPumpView

app_name = 'watering_system'

urlpatterns = [
    path('turn-on/', login_required(TurnOnPumpView.as_view()), name='turn_on_pump'),
    path('turn-off/', login_required(TurnOffPumpView.as_view()), name='turn_off_pump'),
    path('status/', login_required(GetPumpStatus.as_view()), name='pump_status'),

    path('schedules-list/', login_required(SchedulesListView.as_view()), name='schedules_list'),
    path('add-schedule/', login_required(ScheduleCreateView.as_view()), name='add_schedule'),
    path(
        'update-schedule/<int:pk>',
        login_required(ScheduleUpdateView.as_view()),
        name='update_schedule',
    ),
    path(
        'delete-schedule/<int:pk>',
        login_required(ScheduleDeleteView.as_view()),
        name='delete_schedule',
    ),

    path('', login_required(PumpControlTemplateView.as_view()), name='index')
]
