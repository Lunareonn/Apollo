import { socket } from "./websocket.js"

(() => {
    const modal = document.getElementById('settings-modal');
    const openBtn = document.getElementById('open-settings');
    const closeBtns = [
        document.getElementById('settings-close'),
        document.getElementById('settings-cancel')
    ];
    const saveBtn = document.getElementById('settings-save');

    const inputs = {
        downloadFolder: document.getElementById('setting-download-folder'),
        client_id: document.getElementById('setting-client-id'),
        client_secret: document.getElementById('setting-client-secret')
    };

    const SETTINGS_KEY = 'apollo_settings_v1';

    function openModal() {
        modal.classList.add('is-active');
    }

    function closeModal() {
        modal.classList.remove('is-active');
    }

    function loadSettings() {
        fetch('/get-settings', {
            method: 'GET'
        })
        .then(response => response.json())
        .then(data => {
            inputs.downloadFolder.value = data.directory || '';
            inputs.client_id.value = data.client_id || '';
            inputs.client_secret.value = data.client_secret || '';
        })
    }

    function saveSettings() {
        fetch('/save-settings', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                directory: inputs.downloadFolder.value,
                client_id: inputs.client_id.value,
                client_secret: inputs.client_secret.value
            })
        })
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
    });

    // save on Enter
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Enter') saveSettings();
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