'use strict';

function run(backup_path, server_host, server_port) {
    console.log('Restoring: ' + backup_path)
    // Creating Our XMLHttpRequest object
    let xhr = new XMLHttpRequest();

    // Making our connection
    let url = 'http://' + server_host + ':' + server_port + '/hooks/ark-restore-ragnarok?restore=' + backup_path + '&output=json';
    xhr.open("GET", url, true);

    // function execute after request is successful
    xhr.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            console.log(this.responseText);
        } else if (this.readyState == 4 && this.status != 200) {
            console.log('Received non-200 status code: ' + this.status);
            console.log(this);
        }
    }
    // Sending our request
    xhr.send();
}

// [ html-demo ]
const main = document.querySelector('#tree-demo');
const info = document.querySelector('#tree-msg');


main.addEventListener('vtree-open', function (evt) {
    info.innerHTML = evt.detail.id + ' is opened';
});

main.addEventListener('vtree-close', function (evt) {
    info.innerHTML = evt.detail.id + ' is closed';
});

main.addEventListener('vtree-select', function (evt) {
    info.innerHTML = evt.detail.id + ' is selected';
});