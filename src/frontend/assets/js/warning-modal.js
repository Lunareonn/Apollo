import { socket } from "./websocket.js"

(() => {
    const modal = document.getElementById('warning-modal');

    function openModal() {
        modal.classList.add('is-active');
    }

    function closeModal() {
        modal.classList.remove('is-active');
    }

    // close when clicking background
    const bg = modal.querySelector('.modal-background');
    bg && bg.addEventListener('click', closeModal);

    // close on ESC
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') closeModal();
    });

    let bodyEl = modal.querySelector('.modal-card-body');
    if (!bodyEl) {
        bodyEl = document.createElement('div');
        bodyEl.className = 'modal-card-body';
        const content = modal.querySelector('.modal-card-body') || modal;
        content.appendChild(bodyEl);
    }

    socket.on("warning", function(data) {
        console.log("signal got")
        bodyEl.innerHTML = `<p class="warning">${data}</p>`;
        openModal();
    });
})();