"""Watering system utils."""
# 3rd-party
from gpiozero import OutputDevice

# Local
from .models import Pump

relay = OutputDevice(15, False)


def turn_on_pump(pump: Pump) -> bool:
    """Turn on pump.

    :return: True on success, False if pump is already working.
    """
    if pump.status == pump.PumpStatuses.ON:
        return False

    relay.on()

    pump.status = pump.PumpStatuses.ON
    pump.save()

    return True


def turn_off_pump(pump: Pump) -> bool:
    """Turn off pump.

    :return: True on success, False if pump is already off.
    """
    if pump.status == pump.PumpStatuses.OFF:
        return False

    relay.off()

    pump.status = pump.PumpStatuses.OFF
    pump.save()

    return True
