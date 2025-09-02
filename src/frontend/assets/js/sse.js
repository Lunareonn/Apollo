const eventSource = new EventSource("/logs");

eventSource.onmessage = function (event) {
    const logsDiv = document.getElementById("logs");
    // logsDiv.innerHTML += `<p>${event.data}</p>`;

    let parsed = null;
    try {
        parsed = JSON.parse(event.data);
    } catch (e) {
        parsed = null;
    }

    if (parsed && parsed.type === "object" && parsed.type) {
        const ev = new CustomEvent("sse-message", { detail: { raw: event.data, json: parsed } });
        document.dispatchEvent(ev);
        return;
    }

    const ev = new CustomEvent('sse-message', { detail: { raw: event.data, json: parsed } });
    document.dispatchEvent(ev);
};

eventSource.onerror = function () {
    console.error("EventSource failed.");
};