document.addEventListener("DOMContentLoaded", () => {
    window.doorOpenerMessagesP = document.getElementById('door_opener_messages');

    window.doorOpenerBtn = document.getElementById('door_opener_btn');
    window.doorStatus = doorStatuses.OPEN;
    doorOpenerBtn.disabled = true;
    checkDoorStatus();

    doorOpenerBtn.addEventListener('click', () => {
        if(doorStatus === doorStatuses.OPEN){
            closeDoor();
        } else if(doorStatus === doorStatuses.CLOSED) {
            openDoor();
        }
    });

    window.doorStatusSocket = new WebSocket(
        'ws://'
        + window.location.hostname
        + ':8001'
        + '/ws/door_status/'
    );

    doorStatusSocket.onmessage = (e) => {
        const data = JSON.parse(e.data);

        updateDoorStatusInfo(data.door_status);
    }
    doorStatusSocket.onclose = (e) => {
        console.error('Door status socket closed unexpectedly');
    }
})

const closeDoor = () => {
    doorOpenerBtn.disabled = true;

    const callback = (xhr) => {
        if(xhr.status >= 400) {
            alert(JSON.parse(xhr.response).message);
            console.error(xhr);
        }
    }

    doorOpenerMessagesP.innerHTML = doorStatuses.CLOSING;
    sendPost({
        url: closeDoorUrl,
        callback: callback
    })
}

const openDoor = () => {
    doorOpenerBtn.disabled = true;

    const callback = (xhr) => {
        if(xhr.status >= 400) {
            alert(JSON.parse(xhr.response).message);
            console.error(xhr);
        }
    }

    doorOpenerMessagesP.innerHTML = doorStatuses.OPENING;
    sendPost({
        url: openDoorUrl,
        callback: callback
    })
}

const checkDoorStatus = () => {
    const callback = (xhr) => {
        if(xhr.status < 400) {
            const status = JSON.parse(xhr.response).door_status;
            updateDoorStatusInfo(status);
        }
    }

    sendGet({
        url: doorStatusUrl,
        callback: callback
    })
}

const updateDoorStatusInfo = (door_status) => {
    if(door_status === doorStatuses.OPEN) {
        doorOpenHandler();
    } else if(door_status === doorStatuses.CLOSED) {
        doorClosedHandler();
    } else if(door_status === doorStatuses.OPENING) {
        doorOpeningHandler();
    } else if(door_status === doorStatuses.CLOSING) {
        doorClosingHandler();
    }
}

const doorOpenHandler = () => {
    doorOpenerBtn.disabled = false;
    doorOpenerMessagesP.innerHTML = doorStatuses.OPEN;
    window.doorStatus = doorStatuses.OPEN;
}

const doorClosedHandler = () => {
    doorOpenerBtn.disabled = false;
    doorOpenerMessagesP.innerHTML = doorStatuses.CLOSED;
    window.doorStatus = doorStatuses.CLOSED;
}

const doorOpeningHandler = () => {
    doorOpenerBtn.disabled = true;
    doorOpenerMessagesP.innerHTML = doorStatuses.OPENING;
    window.doorStatus = doorStatuses.OPENING;
}

const doorClosingHandler = () => {
    doorOpenerBtn.disabled = true;
    doorOpenerMessagesP.innerHTML = doorStatuses.CLOSING;
    window.doorStatus = doorStatuses.CLOSING;
}
