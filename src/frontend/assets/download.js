document.getElementById("trigger-btn").addEventListener("click", function () {
    fetch("/download", {
        method: "POST",
        headers: {
            'Content-Type': 'application/json'
        }
    })
        .then(response => response.json())
        .then(data => {
            document.getElementById("response").textContent = data.message || 'Success';
        })
        .catch(error => {
            document.getElementById('response').textContent = "Error";
            console.error(error);
        });
});