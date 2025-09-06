document.getElementById("trigger-btn").addEventListener("click", function () {
    const queryInput = document.getElementById("query-input");
    const query = queryInput ? queryInput.value : "";
    var socket = io();

    socket.emit("download", { args: [query] })

    // fetch("/download", {
    //     method: "POST",
    //     headers: {
    //         'Content-Type': 'application/json'
    //     },
    //     body: JSON.stringify({query})
    // })
    //     .then(response => response.json())
    //     .then(data => {
    //         document.getElementById("response").textContent = data.message || 'Success';
    //     })
    //     .catch(error => {
    //         document.getElementById('response').textContent = "Error";
    //         console.error(error);
    //     });
});