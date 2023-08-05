"""Door opener tasks."""
# Standard Library
import time

# 3rd-party
from celery import shared_task

# Local
from .models import Pump
from .utils import turn_off_pump
from .utils import turn_on_pump


@shared_task
def turn_on_pump_task(pump_pk: int) -> None:
    """Turn on pump for period of time set in model."""
    pump = Pump.objects.get(pk=pump_pk)

    sleep_time = pump.pumping_time

    turn_on_pump(pump)
    time.sleep(sleep_time)
    turn_off_pump(pump)
