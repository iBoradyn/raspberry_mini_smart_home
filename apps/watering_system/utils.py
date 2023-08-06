"""Watering system utils."""
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
# 3rd-party
from gpiozero import OutputDevice

# Local
from .models import Pump
from apps.core.utils import flush_tasks_by_name

relay = OutputDevice(15, False)


def send_status_to_consumers(status):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        'pump_status',
        {'type': 'pump.status', 'pump_status': status},
    )


def turn_on_pump(pump: Pump) -> bool:
    """Turn on pump.

    :return: True on success, False if pump is already working.
    """
    if pump.status == pump.PumpStatuses.ON:
        return False

    relay.on()

    pump.status = pump.PumpStatuses.ON
    pump.save()

    send_status_to_consumers(pump.get_status_display())

    return True


def turn_off_pump(pump: Pump, flush_tasks=True) -> bool:
    """Turn off pump.

    :return: True on success, False if pump is already off.
    """
    if pump.status == pump.PumpStatuses.OFF:
        return False

    from .tasks import turn_on_pump_task

    relay.off()

    if flush_tasks:
        pump.status = pump.PumpStatuses.TURNING_OFF
        pump.save()
        send_status_to_consumers(pump.get_status_display())

        flush_tasks_by_name(turn_on_pump_task.__module__, turn_on_pump_task.__name__)

    pump.status = pump.PumpStatuses.OFF
    pump.save()
    send_status_to_consumers(pump.get_status_display())

    return True
