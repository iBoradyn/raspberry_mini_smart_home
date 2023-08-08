"""Door opener utils."""
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
# 3rd-party
from gpiozero import OutputDevice

# Local
from .models import Motor
from apps.core.utils import flush_tasks_by_name

relayLeft = OutputDevice(17, False)
relayRight = OutputDevice(22, False)


def send_status_to_consumers(status):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        'door_status',
        {'type': 'door.status', 'door_status': status},
    )


def spin_motor_left(motor: Motor) -> bool:
    """Start spinning motor in 'left' direction.

    :return: True on success, False if motor is already spinning in that direction.
    """
    if motor.status == motor.MotorStatuses.LEFT_SPINNING:
        return False

    relayRight.off()
    relayLeft.on()

    motor.door_status = motor.DoorStatuses.CLOSING
    motor.status = motor.MotorStatuses.LEFT_SPINNING
    motor.save()

    send_status_to_consumers(motor.door_status)

    return True


def spin_motor_right(motor: Motor) -> bool:
    """Start spinning motor in 'right' direction.

    :return: True on success, False if motor is already spinning in that direction.
    """
    if motor.status == motor.MotorStatuses.RIGHT_SPINNING:
        return False

    relayLeft.off()
    relayRight.on()

    motor.door_status = motor.DoorStatuses.OPENING
    motor.status = motor.MotorStatuses.RIGHT_SPINNING
    motor.save()

    send_status_to_consumers(motor.door_status)

    return True


def turn_off_motor(motor: Motor, flush_tasks=True) -> bool:
    """Turn off motor.

    :return: True on success, False if motor is already turned off.
    """
    if motor.status == motor.MotorStatuses.NO_SPINNING or \
            motor.status == motor.MotorStatuses.TURNING_OFF_SPINNING:
        return False

    from .tasks import spin_motor

    relayLeft.off()
    relayRight.off()

    if flush_tasks:
        motor.status = motor.MotorStatuses.TURNING_OFF_SPINNING
        motor.save()

        flush_tasks_by_name(spin_motor.__module__, spin_motor.__name__)

    if motor.door_status == motor.DoorStatuses.CLOSING:
        motor.door_status = motor.DoorStatuses.CLOSED
    else:
        motor.door_status = motor.DoorStatuses.OPEN
    motor.status = motor.MotorStatuses.NO_SPINNING
    motor.save()
    send_status_to_consumers(motor.door_status)

    return True
