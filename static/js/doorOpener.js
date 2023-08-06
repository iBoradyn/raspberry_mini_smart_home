document.addEventListener("DOMContentLoaded", () => {
    window.doorOpenerMessagesP = document.getElementById('door_opener_messages');

    window.spinMotorLeftBtn = document.getElementById('spin_left_btn');
    window.spinMotorRightBtn = document.getElementById('spin_right_btn');
    window.turnMotorOffBtn = document.getElementById('spin_off_btn');
    turnMotorOffBtn.disabled = true;

    spinMotorLeftBtn.addEventListener('click', spinMotorLeft);
    spinMotorRightBtn.addEventListener('click', spinMotorRight);
    turnMotorOffBtn.addEventListener('click', turnMotorOff);

    checkMotorStatus();
    window.motorStatusSocket = new WebSocket(
        'ws://'
        + window.location.hostname
        + ':8001'
        + '/ws/motor_status/'
    );

    motorStatusSocket.onmessage = (e) => {
        const data = JSON.parse(e.data);

        updateMotorStatusInfo(data.motor_status);
    }
    motorStatusSocket.onclose = (e) => {
        console.error('Motor status socket closed unexpectedly');
    }
})

const spinMotorLeft = () => {
    disableMotorButtons();

    const callback = (xhr) => {
        if(xhr.status >= 400) {
            alert(JSON.parse(xhr.response).message);
            console.error(xhr);
        }
    }

    doorOpenerMessagesP.innerHTML = 'Starting spinning motor...';
    sendPost({
        url: spinMotorLeftUrl,
        callback: callback
    })
}

const spinMotorRight = () => {
    disableMotorButtons();

    const callback = (xhr) => {
        if(xhr.status >= 400) {
            alert(JSON.parse(xhr.response).message);
            console.error(xhr);
        }
    }

    doorOpenerMessagesP.innerHTML = 'Starting spinning motor...';
    sendPost({
        url: spinMotorRightUrl,
        callback: callback
    })
}

const turnMotorOff = () => {
    disableMotorButtons();

    const callback = (xhr) => {
        if(xhr.status >= 400) {
            alert(JSON.parse(xhr.response).message);
            console.error(xhr);
        }
    }

    doorOpenerMessagesP.innerHTML = 'Stopping motor...';
    sendPost({
        url: turnOffMotor,
        callback: callback
    })
}

const checkMotorStatus = () => {
    const callback = (xhr) => {
        if(xhr.status < 400) {
            const status = JSON.parse(xhr.response).motor_status;
            updateMotorStatusInfo(status);
        }
    }

    sendGet({
        url: motorStatusUrl,
        callback: callback
    })
}

const updateMotorStatusInfo = (motor_status) => {
    if(motor_status === motorStatuses.LEFT) {
        motorSpinningLeftHandler();
    } else if(motor_status === motorStatuses.RIGHT) {
        motorSpinningRightHandler();
    } else if(motor_status === motorStatuses.TURNING_OFF) {
        motorTurningOffHandler();
    } else if(motor_status === motorStatuses.OFF) {
        motorOffHandler();
    }
}

const disableMotorButtons = () => {
    turnMotorOffBtn.disabled = true;
    spinMotorRightBtn.disabled = true;
    spinMotorLeftBtn.disabled = true;
}

const motorSpinningLeftHandler = () => {
    doorOpenerMessagesP.innerHTML = 'Motor spinning left.'

    turnMotorOffBtn.disabled = false;
    spinMotorRightBtn.disabled = false;
    spinMotorLeftBtn.disabled = true;
}

const motorSpinningRightHandler = () => {
    doorOpenerMessagesP.innerHTML = 'Motor spinning right.'

    turnMotorOffBtn.disabled = false;
    spinMotorRightBtn.disabled = true;
    spinMotorLeftBtn.disabled = false;
}

const motorTurningOffHandler = () => {
    doorOpenerMessagesP.innerHTML = 'Motor turning off.'

    turnMotorOffBtn.disabled = true;
    spinMotorRightBtn.disabled = true;
    spinMotorLeftBtn.disabled = true;
}

const motorOffHandler = () => {
    doorOpenerMessagesP.innerHTML = 'Motor stopped.'

    turnMotorOffBtn.disabled = true;
    spinMotorRightBtn.disabled = false;
    spinMotorLeftBtn.disabled = false;
}
