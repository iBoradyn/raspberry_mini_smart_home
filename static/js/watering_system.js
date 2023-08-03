window.addEventListener("load", () => {
    let pumpOn = false;
    const btn = document.getElementById('watering_btn');

    btn.addEventListener('click', () => {
        let url = turnOnPumpUrl;
        if(pumpOn) {
            url = turnOffPumpUrl;
        }
        let xhr = new XMLHttpRequest();

        xhr.open("POST", url, true);
        xhr.setRequestHeader('X-CSRFToken', csrfToken);
        xhr.onreadystatechange = function () {
            if(this.status < 400) {
                pumpOn = !pumpOn;

                if(pumpOn) {
                    btn.innerHTML = 'Stop';
                } else {
                    btn.innerHTML = 'Start';
                }
            }
        }

        xhr.send();
    })
})
