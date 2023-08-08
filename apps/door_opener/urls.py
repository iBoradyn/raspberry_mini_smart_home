"""Door opener urls."""
# Django
from django.contrib.auth.decorators import login_required
from django.urls import path

# Local
from .views import GetDoorStatus, MotorControlTemplateView
from .views import CloseDoorView
from .views import OpenDoorView

app_name = 'door_opener'

urlpatterns = [
    path(
        'close-door/',
        login_required(CloseDoorView.as_view()),
        name='close_door',
    ),
    path(
        'open-door/',
        login_required(OpenDoorView.as_view()),
        name='open_door',
    ),
    path('status/', login_required(GetDoorStatus.as_view()), name='door_status'),

    path('', login_required(MotorControlTemplateView.as_view()), name='index')
]
