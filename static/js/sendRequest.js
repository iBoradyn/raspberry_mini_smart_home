const sendPost = ({
    url,
    data = {},
    callback = () => {},
}) => {
    let xhr = new XMLHttpRequest();

    xhr.open("POST", url, true);
    xhr.setRequestHeader('X-CSRFToken', csrfToken);
    xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    xhr.onreadystatechange = () => {
        if(xhr.readyState === 4) {
            callback(xhr);
        }
    }

    xhr.send(JSON.stringify(data));
}


const sendGet = ({
    url,
    callback = () => {},
}) => {
    let xhr = new XMLHttpRequest();

    xhr.open("GET", url, true);
    xhr.setRequestHeader('X-CSRFToken', csrfToken);
    xhr.onreadystatechange = () => {
        if(xhr.readyState === 4) {
            callback(xhr);
        }
    }

    xhr.send();
}