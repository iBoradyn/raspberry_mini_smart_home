"""Door opener urls."""
# Django
from django.contrib.auth.decorators import login_required
from django.urls import path

# Local
from .views import TurnMotorLeftSpinningView
from .views import TurnMotorOffView
from .views import TurnMotorRightSpinningView

app_name = 'door_opener'

urlpatterns = [
    path(
        'turn-left/',
        login_required(TurnMotorLeftSpinningView.as_view()),
        name='spin_motor_left',
    ),
    path(
        'turn-right/',
        login_required(TurnMotorRightSpinningView.as_view()),
        name='spin_motor_right',
    ),
    path('turn-off/', login_required(TurnMotorOffView.as_view()), name='turn_motor_off'),
]
