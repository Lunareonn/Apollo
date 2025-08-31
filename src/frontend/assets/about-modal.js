(() => {
    const modal = document.getElementById('about-modal');
    const openBtn = document.getElementById('open-about');
    const closeBtns = [
        document.getElementById('about-close')
    ];

    function openModal() {
        modal.classList.add('is-active');
    }

    function closeModal() {
        modal.classList.remove('is-active');
    }

    openBtn && openBtn.addEventListener('click', (e) => {
        e.preventDefault();
        openModal();
    });

    closeBtns.forEach(btn => btn && btn.addEventListener('click', (e) => {
        e.preventDefault();
        closeModal();
    }));

    // close when clicking background
    const bg = modal.querySelector('.modal-background');
    bg && bg.addEventListener('click', closeModal);

    // close on ESC
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') closeModal();
    });
})();