document.addEventListener("DOMContentLoaded", () => {
    window.pumpStatus = pumpStatuses.OFF;
    checkPumpStatus();

    window.wateringSwitchBtn = document.getElementById('watering_btn');
    window.wateringSystemMessagesP = document.getElementById('watering_system_messages');

    wateringSwitchBtn.addEventListener('click', switchPump);

    window.pumpStatusSocket = new WebSocket(
        'ws://'
        + window.location.hostname
        + ':8001'
        + '/ws/pump_status/'
    );

    pumpStatusSocket.onmessage = (e) => {
        const data = JSON.parse(e.data);

        updatePumpStatusInfo(data.pump_status);
    }
    pumpStatusSocket.onclose = (e) => {
        console.error('Pump status socket closed unexpectedly');
    }
})

const switchPump = () => {
    let url = turnOnPumpUrl;
    let message = 'Starting pump...'
    if(pumpStatus === pumpStatuses.ON) {
        url = turnOffPumpUrl;
        message = 'Stopping pump...'
    }

    const callback = (xhr) => {
        if(xhr.status >= 400) {
            alert(JSON.parse(xhr.response).message);
            console.error(xhr)
        }
    }

    wateringSystemMessagesP.innerHTML = message;
    sendPost({
        url: url,
        callback: callback
    })
}

const checkPumpStatus = () => {
    const callback = (xhr) => {
        if(xhr.status < 400) {
            const status = JSON.parse(xhr.response).pump_status;
            updatePumpStatusInfo(status);
        }
    }

    sendGet({
        url: pumpStatusUrl,
        callback: callback
    })
}

const updatePumpStatusInfo = (pump_status) => {
    if(pump_status === pumpStatuses.OFF) {
        pumpOffHandler();
    } else if(pump_status === pumpStatuses.ON) {
        pumpOnHandler();
    } else if (pump_status === pumpStatuses.TURNING_OFF) {
        pumpTurningOffHandler();
    }
}

const pumpOnHandler = () => {
    window.pumpStatus = pumpStatuses.ON;
    wateringSystemMessagesP.innerHTML = 'Pump working.';
    wateringSwitchBtn.innerHTML = 'Stop';
    wateringSwitchBtn.disabled = false;
}

const pumpTurningOffHandler = () => {
    window.pumpStatus = pumpStatuses.TURNING_OFF;
    wateringSystemMessagesP.innerHTML = 'Stopping pump....';
    wateringSwitchBtn.innerHTML = 'Stop';
    wateringSwitchBtn.disabled = true;
}

const pumpOffHandler = () => {
    window.pumpStatus = pumpStatuses.OFF;
    wateringSystemMessagesP.innerHTML = 'Pump stopped.';
    wateringSwitchBtn.innerHTML = 'Start';
    wateringSwitchBtn.disabled = false;
}
