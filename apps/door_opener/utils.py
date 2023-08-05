"""Door opener utils."""
# 3rd-party
from gpiozero import OutputDevice

# Local
from .models import Motor

relayLeft = OutputDevice(17, False)
relayRight = OutputDevice(22, False)


def spin_motor_left(motor: Motor) -> bool:
    """Start spinning motor in 'left' direction.

    :return: True on success, False if motor is already spinning in that direction.
    """
    if motor.status == motor.MotorStatuses.LEFT_SPINNING:
        return False

    relayRight.off()
    relayLeft.on()

    motor.status = motor.MotorStatuses.LEFT_SPINNING
    motor.save()

    return True


def spin_motor_right(motor: Motor) -> bool:
    """Start spinning motor in 'right' direction.

    :return: True on success, False if motor is already spinning in that direction.
    """
    if motor.status == motor.MotorStatuses.RIGHT_SPINNING:
        return False

    relayLeft.off()
    relayRight.on()

    motor.status = motor.MotorStatuses.RIGHT_SPINNING
    motor.save()

    return True


def turn_off_motor(motor: Motor) -> bool:
    """Turn off motor.

    :return: True on success, False if motor is already turned off.
    """
    if motor.status == motor.MotorStatuses.NO_SPINNING:
        return False

    relayLeft.off()
    relayRight.off()

    motor.status = motor.MotorStatuses.NO_SPINNING
    motor.save()

    return True
