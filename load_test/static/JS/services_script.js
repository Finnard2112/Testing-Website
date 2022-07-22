
function setCookie(cname, cvalue, exdays) {
    const d = new Date();
    d.setTime(d.getTime() + (exdays*24*60*60*1000));
    let expires = "expires="+ d.toUTCString();
    document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
  }
  
function start_service(service_name, play_link) {
    var xhr = new XMLHttpRequest();
    xhr.onload = function () {
        const response = JSON.parse(this.responseText);
        if (response.message == "success") {
            setCookie(service_name, response.session_id, 30);
        } else {
            alert("Unable to start" + service_name);
        }
    }
    xhr.open("POST", play_link);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.send();
    return xhr.status;
}

function getCookie(cname) {
    let name = cname + "=";
    let decodedCookie = decodeURIComponent(document.cookie);
    let ca = decodedCookie.split(';');
    for(let i = 0; i <ca.length; i++) {
        let c = ca[i];
        while (c.charAt(0) == ' ') {
        c = c.substring(1);
        }
        if (c.indexOf(name) == 0) {
        return c.substring(name.length, c.length);
        }
    }
    return "";
}

function status_check(name, session_id) {
    var xhr = new XMLHttpRequest();
        xhr.onload = function () {
            const response = JSON.parse(this.responseText);
            service_status = "#"+name+"-status"
            current_id = "#" + name + "-button"
            if (response.status == 0) {
                document.getElementById(service_status).className = "active";
                document.getElementById(service_status).textContent = "Đang chạy"
                if (!($(current_id).hasClass('paused'))) {
                    $(current_id).toggleClass('paused');
                }
            } else if (response.status == 1) {
                document.getElementById(service_status).className = "completed";
                document.getElementById(service_status).textContent = "Đã hoàn thành"
                if (($(current_id).hasClass('paused'))) {
                    ($(current_id).toggleClass('paused'));
                }
            }
        }
    xhr.open("GET", "https://192.168.41.199:8090/status_service/"+ session_id);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.send();
}