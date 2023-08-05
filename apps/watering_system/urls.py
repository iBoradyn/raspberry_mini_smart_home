"""Watering system urls."""
# Django
from django.contrib.auth.decorators import login_required
from django.urls import path

# Local
from .views import GetPumpStatus
from .views import TurnOffPumpView
from .views import TurnOnPumpView

app_name = 'watering_system'

urlpatterns = [
    path('turn-on/', login_required(TurnOnPumpView.as_view()), name='turn_on_pump'),
    path('turn-off/', login_required(TurnOffPumpView.as_view()), name='turn_off_pump'),
    path('status/', login_required(GetPumpStatus.as_view()), name='pump_status'),
]
