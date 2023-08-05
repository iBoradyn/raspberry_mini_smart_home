document.addEventListener("DOMContentLoaded", () => {
    window.pumpStatus = pumpStatuses.OFF;
    checkPumpStatus();
    setInterval(checkPumpStatus, 10000);

    window.wateringSwitchBtn = document.getElementById('watering_btn');
    window.wateringSystemMessagesP = document.getElementById('watering_system_messages');

    wateringSwitchBtn.addEventListener('click', switchPump)
})

const switchPump = () => {
    let url = turnOnPumpUrl;
    let message = 'Starting pump...';
    if(pumpStatus === pumpStatuses.ON) {
        url = turnOffPumpUrl;
        message = 'Stopping pump...';
    }

    const callback = (xhr) => {
        if(xhr.status < 400) {
            if(pumpStatus === pumpStatuses.ON) {
                pumpOnHandler();
            } else {
                pumpOffHandler();
            }
        } else {
            wateringSystemMessagesP.innerHTML = 'ERROR! Check pump.';
            alert(JSON.parse(xhr.response.message));
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

            if(status === pumpStatuses.OFF) {
                pumpOffHandler();
            } else if(status === pumpStatuses.ON) {
                pumpOnHandler();
            }
        }
    }

    sendGet({
        url: pumpStatusUrl,
        callback: callback
    })
}

const pumpOnHandler = () => {
    window.pumpStatus = pumpStatuses.ON;
    wateringSystemMessagesP.innerHTML = 'Pump working.';
    wateringSwitchBtn.innerHTML = 'Stop';
}

const pumpOffHandler = () => {
    window.pumpStatus = pumpStatuses.OFF;
    wateringSystemMessagesP.innerHTML = 'Pump stopped.';
    wateringSwitchBtn.innerHTML = 'Start';
}