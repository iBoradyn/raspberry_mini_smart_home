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
    setInterval(checkMotorStatus, 10000);
})

const spinMotorLeft = () => {
    disableMotorButtons();

    const callback = (xhr) => {
        if(xhr.status < 400) {
            motorSpinningLeftHandler();
        } else {
            motorErrorHandler(JSON.parse(xhr.response.message));
        }
    }

    doorOpenerMessagesP.innerHTML = 'Starting spinning motor...'
    sendPost({
        url: spinMotorLeftUrl,
        callback: callback
    })
}

const spinMotorRight = () => {
    disableMotorButtons();

    const callback = (xhr) => {
        if(xhr.status < 400) {
            motorSpinningRightHandler();
        } else {
            motorErrorHandler(JSON.parse(xhr.response.message));
        }

    }

    doorOpenerMessagesP.innerHTML = 'Starting spinning motor...'
    sendPost({
        url: spinMotorRightUrl,
        callback: callback
    })
}

const turnMotorOff = () => {
    disableMotorButtons();

    const callback = (xhr) => {
        if(xhr.status < 400) {
            motorOffHandler();
        } else {
            motorErrorHandler(JSON.parse(xhr.response.message));
        }
    }

    doorOpenerMessagesP.innerHTML = 'Stopping motor...'
    sendPost({
        url: turnOffMotor,
        callback: callback
    })
}

const checkMotorStatus = () => {
    const callback = (xhr) => {
        if(xhr.status < 400) {
            const status = JSON.parse(xhr.response).motor_status;

            if(status === motorStatuses.LEFT) {
                motorSpinningLeftHandler();
            } else if(status === motorStatuses.RIGHT) {
                motorSpinningRightHandler();
            } else if(status === motorStatuses.OFF) {
                motorOffHandler();
            }
        }
    }

    sendGet({
        url: motorStatusUrl,
        callback: callback
    })
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

const motorOffHandler = () => {
    doorOpenerMessagesP.innerHTML = 'Motor stopped.'

    turnMotorOffBtn.disabled = true;
    spinMotorRightBtn.disabled = false;
    spinMotorLeftBtn.disabled = false;
}

const motorErrorHandler = (message) => {
    doorOpenerMessagesP.innerHTML = 'ERROR! Check motor.'

    turnMotorOffBtn.disabled = false;
    spinMotorRightBtn.disabled = true;
    spinMotorLeftBtn.disabled = true;

    alert(message);

}