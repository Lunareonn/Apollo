var socket = io();

const logsDiv = document.getElementById("logs");

socket.on("message", function(data) {
    logsDiv.innerHTML += `<p>${data}</p>`;
});