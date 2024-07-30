'use strict';

function run(answer, server_host, server_port) {
    console.log('Running: ' + answer)
    // Creating Our XMLHttpRequest object
    let xhr = new XMLHttpRequest();

    // Making our connection
    let url = 'http://' + server_host + ':' + server_port + '/hooks/ark-servers?server=ragnarok&output=json';
    xhr.open("GET", url, true);

    // function execute after request is successful
    xhr.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            console.log(this.responseText);
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