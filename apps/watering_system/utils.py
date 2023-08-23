"""Watering system utils."""
# 3rd-party
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from gpiozero import OutputDevice

# Project
from apps.core.utils import flush_tasks_by_name

# Local
from .models import Pump

relay = OutputDevice(15, False)


def send_status_to_consumers(status):  # noqa: D103
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        'pump_status',
        {'type': 'pump.status', 'pump_status': status},
    )


def turn_on_pump(pump: Pump) -> bool:  # noqa: D103
    """Turn on pump.

    :return: True on success, False if pump is already working.
    """
    if pump.status == pump.PumpStatuses.ON:
        return False

    relay.on()

    pump.status = pump.PumpStatuses.ON
    pump.save()

    send_status_to_consumers(pump.status)

    return True


def turn_off_pump(pump: Pump, flush_tasks=True) -> bool:  # noqa: D103
    """Turn off pump.

    :return: True on success, False if pump is already off.
    """
    if pump.status == pump.PumpStatuses.OFF:
        return False

    # Local
    from .tasks import turn_on_pump_task

    relay.off()

    if flush_tasks:
        pump.status = pump.PumpStatuses.TURNING_OFF
        pump.save()
        send_status_to_consumers(pump.status)

        flush_tasks_by_name(turn_on_pump_task.__module__, turn_on_pump_task.__name__)

    pump.status = pump.PumpStatuses.OFF
    pump.save()
    send_status_to_consumers(pump.status)

    return True
