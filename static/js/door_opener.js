window.addEventListener("load", () => {
    window.spinMotorLeftBtn = document.getElementById('spin_left_btn');
    window.spinMotorRightBtn = document.getElementById('spin_right_btn');
    window.turnMotorOffBtn = document.getElementById('spin_off_btn');
    turnMotorOffBtn.disabled = true;

    spinMotorLeftBtn.addEventListener('click', spinMotorLeft)
    spinMotorRightBtn.addEventListener('click', spinMotorRight)
    turnMotorOffBtn.addEventListener('click', turnMotorOff)
})

const spinMotorLeft = () => {
    let xhr = new XMLHttpRequest();

    xhr.open("POST", spinMotorLeftUrl, true);
    xhr.setRequestHeader('X-CSRFToken', csrfToken);
    xhr.onreadystatechange = function () {
        if(this.status < 400) {
            turnMotorOffBtn.disabled = false;
            spinMotorRightBtn.disabled = false;
            spinMotorLeftBtn.disabled = true;
        }
    }

    xhr.send();
}

const spinMotorRight = () => {
    let xhr = new XMLHttpRequest();

    xhr.open("POST", spinMotorRightUrl, true);
    xhr.setRequestHeader('X-CSRFToken', csrfToken);
    xhr.onreadystatechange = function () {
        if(this.status < 400) {
            turnMotorOffBtn.disabled = false;
            spinMotorRightBtn.disabled = true;
            spinMotorLeftBtn.disabled = false;
        }
    }

    xhr.send();
}

const turnMotorOff = () => {
    let xhr = new XMLHttpRequest();

    xhr.open("POST", turnOffMotor, true);
    xhr.setRequestHeader('X-CSRFToken', csrfToken);
    xhr.onreadystatechange = function () {
        if(this.status < 400) {
            turnMotorOffBtn.disabled = true;
            spinMotorRightBtn.disabled = false;
            spinMotorLeftBtn.disabled = false;
        }
    }

    xhr.send();
}