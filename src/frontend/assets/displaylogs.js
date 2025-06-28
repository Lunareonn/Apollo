const eventSource = new EventSource("/logs");

eventSource.onmessage = function (event) {
    const logsDiv = document.getElementById("logs");
    logsDiv.innerHTML += `<p>${event.data}</p>`;
};

eventSource.onerror = function () {
    console.error("EventSource failed.");
};