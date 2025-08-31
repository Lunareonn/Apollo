(() => {
    const modal = document.getElementById('settings-modal');
    const openBtn = document.getElementById('open-settings');
    const closeBtns = [
        document.getElementById('settings-close'),
        document.getElementById('settings-cancel')
    ];
    const saveBtn = document.getElementById('settings-save');

    const inputs = {
        downloadFolder: document.getElementById('setting-download-folder')
    };

    const SETTINGS_KEY = 'apollo_settings_v1';

    function openModal() {
        modal.classList.add('is-active');
    }

    function closeModal() {
        modal.classList.remove('is-active');
    }

    function loadSettings() {
        const raw = localStorage.getItem(SETTINGS_KEY);
        if (!raw) return;
        try {
            const s = JSON.parse(raw);
            if (s.downloadFolder) inputs.downloadFolder.value = s.downloadFolder;
            if (s.maxConcurrent) inputs.maxConcurrent.value = s.maxConcurrent;
            inputs.verboseLogs.checked = !!s.verboseLogs;
        } catch (e) {
            console.warn('Failed to parse settings', e);
        }
    }

    function saveSettings() {
        const s = {
            downloadFolder: inputs.downloadFolder.value || '',
            maxConcurrent: parseInt(inputs.maxConcurrent.value, 10) || 1,
            verboseLogs: !!inputs.verboseLogs.checked
        };
        localStorage.setItem(SETTINGS_KEY, JSON.stringify(s));
    }

    openBtn && openBtn.addEventListener('click', (e) => {
        e.preventDefault();
        loadSettings();
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

    saveBtn && saveBtn.addEventListener('click', (e) => {
        e.preventDefault();
        saveSettings();
        closeModal();
    });

    // Optional: expose settings for other scripts
    window.apolloSettings = {
        get: () => {
            try {
                return JSON.parse(localStorage.getItem(SETTINGS_KEY)) || {};
            } catch {
                return {};
            }
        }
    };
})();