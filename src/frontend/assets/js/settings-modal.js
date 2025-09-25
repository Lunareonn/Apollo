import { socket } from "./websocket.js"

(() => {
    const modal = document.getElementById('settings-modal');
    const openBtn = document.getElementById('open-settings');
    const closeBtns = [
        document.getElementById('settings-close'),
        document.getElementById('settings-cancel')
    ];
    const saveBtn = document.getElementById('settings-save');
    const savedText = document.getElementById('settings-saved-status')

    const inputs = {
        downloadFolder: document.getElementById('setting-download-folder'),
        client_id: document.getElementById('setting-client-id'),
        client_secret: document.getElementById('setting-client-secret'),
        min_silence_len: document.getElementById('setting-min-silence-len'),
        silence_thresh: document.getElementById('setting-silence-thresh')
    };

    const SETTINGS_KEY = 'apollo_settings_v1';

    function openModal() {
        savedText.textContent = '';
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
            inputs.min_silence_len.value = data.min_silence_len || '1000';
            inputs.silence_thresh.value = data.silence_thresh || '-50';
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
                client_secret: inputs.client_secret.value,
                min_silence_len: parseInt(inputs.min_silence_len.value),
                silence_thresh: parseInt(inputs.silence_thresh.value)
            })
        }).then(response => response.json()).then(data => {
            console.log(data);
            savedText.textContent = data.status;
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
})();