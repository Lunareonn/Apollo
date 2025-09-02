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

    document.addEventListener('sse-message', (ev) => {
        const { json } = ev.detail || {};
        if (json && json.type === 'modal' && json.modal === 'warning') {
            bodyEl.textContent = json.message || '';
            openModal();
        }
    });
})();