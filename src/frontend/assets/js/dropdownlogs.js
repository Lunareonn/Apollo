document.addEventListener("DOMContentLoaded", function () {
    const toggle = document.getElementById("log-toggle");
    const content = document.getElementById("log-content");

    if (toggle && content) {
        toggle.addEventListener("click", function () {
            content.classList.toggle("expanded")
        });
    }
});