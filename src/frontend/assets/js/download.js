import { socket } from "./websocket.js"

document.getElementById("trigger-btn").addEventListener("click", function () {
    const queryInput = document.getElementById("query-input");
    const query = queryInput ? queryInput.value : "";

    socket.emit("download", query)
});