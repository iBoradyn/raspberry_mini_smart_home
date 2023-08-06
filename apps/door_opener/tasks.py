"""Door opener tasks."""
# Standard Library
import time

# 3rd-party
from celery import shared_task

# Local
from .models import Motor
from .utils import spin_motor_left
from .utils import spin_motor_right
from .utils import turn_off_motor


@shared_task
def spin_motor(motor_pk: int, direction: str) -> None:
    """Spin motor in given direction for period of time set in model."""
    motor = Motor.objects.get(pk=motor_pk)

    sleep_time = 0
    if direction == 'left':
        sleep_time = motor.left_spinning_time
        spin_motor_left(motor)
    elif direction == 'right':
        sleep_time = motor.right_spinning_time
        spin_motor_right(motor)

    time.sleep(sleep_time)
    turn_off_motor(motor, flush_tasks=False)
