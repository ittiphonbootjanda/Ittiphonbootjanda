/**
 * Drive Terminal Creator Edition - app.js
 */

const CLIENT_ID = 'YOUR_GOOGLE_CLIENT_ID.apps.googleusercontent.com';
const SCOPES = 'https://www.googleapis.com/auth/drive.file https://www.googleapis.com/auth/drive.metadata.readonly';

let accessToken = null;
let tokenClient;
let currentEditingFileId = null;

// 1. Terminal Setup
const term = new Terminal({ cursorBlink: true, fontSize: 14, theme: { background: '#000', foreground: '#0f0' } });
const fitAddon = new FitAddon.FitAddon();
term.loadAddon(fitAddon);
term.open(document.getElementById('terminal-container'));
fitAddon.fit();

// 2. Emulator Setup
let emulator = new V86Starter({
    wasm_path: "https://copy.sh/v86/v86.wasm",
    memory_size: 256 * 1024 * 1024,
    screen_container: document.getElementById('screen-container'),
    bios: { url: "https://copy.sh/v86/bios/seabios.bin" },
    vga_bios: { url: "https://copy.sh/v86/bios/vgabios.bin" },
    cdrom: { url: "https://copy.sh/v86/images/alpine.iso" },
    network_relay_url: "wss://relay.widgetry.org/",
    autostart: true,
});
emulator.add_listener("serial0-output-char", (char) => term.write(char));
term.onData(data => { for(let i=0; i<data.length; i++) emulator.serial0_send(data.charCodeAt(i)); });

// 3. Drive Explorer & Editor Logic
async function listDriveFiles() {
    if (!accessToken) return;
    const res = await fetch('https://www.googleapis.com/drive/v3/files?pageSize=30&fields=files(id, name, mimeType)', {
        headers: { 'Authorization': `Bearer ${accessToken}` }
    });
    const data = await res.json();
    const list = document.getElementById('file-list');
    list.innerHTML = '';
    data.files.forEach(file => {
        const li = document.createElement('li');
        li.textContent = (file.mimeType.includes('folder') ? '📁 ' : '📄 ') + file.name;
        li.onclick = () => {
            if (!file.mimeType.includes('folder')) openInEditor(file);
        };
        list.appendChild(li);
    });
}

async function openInEditor(file) {
    const res = await fetch(`https://www.googleapis.com/drive/v3/files/${file.id}?alt=media`, {
        headers: { 'Authorization': `Bearer ${accessToken}` }
    });
    const text = await res.text();
    document.getElementById('editor-textarea').value = text;
    document.getElementById('editing-filename').textContent = file.name;
    currentEditingFileId = file.id;
    document.getElementById('editor-overlay').style.display = 'flex';
}

async function saveFileToDrive() {
    if (!accessToken) return;
    const content = document.getElementById('editor-textarea').value;
    const filename = document.getElementById('editing-filename').textContent;
    
    const metadata = { name: filename, mimeType: 'text/plain' };
    const blob = new Blob([content], { type: 'text/plain' });
    const formData = new FormData();
    formData.append('metadata', new Blob([JSON.stringify(metadata)], { type: 'application/json' }));
    formData.append('file', blob);

    let url = 'https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart';
    let method = 'POST';
    if (currentEditingFileId) {
        url = `https://www.googleapis.com/upload/drive/v3/files/${currentEditingFileId}?uploadType=multipart`;
        method = 'PATCH';
    }

    const res = await fetch(url, { method, headers: { 'Authorization': `Bearer ${accessToken}` }, body: formData });
    if (res.ok) {
        alert("File saved to Google Drive!");
        listDriveFiles();
    }
}

// 4. UI Events
document.getElementById('new-file').onclick = () => {
    const name = prompt("Enter new filename:", "new_script.py");
    if (name) {
        document.getElementById('editor-textarea').value = "";
        document.getElementById('editing-filename').textContent = name;
        currentEditingFileId = null;
        document.getElementById('editor-overlay').style.display = 'flex';
    }
};

document.getElementById('save-editor').onclick = saveFileToDrive;
document.getElementById('close-editor').onclick = () => document.getElementById('editor-overlay').style.display = 'none';
document.getElementById('toggle-explorer').onclick = () => {
    const exp = document.getElementById('drive-explorer');
    exp.style.display = exp.style.display === 'flex' ? 'none' : 'flex';
    if (exp.style.display === 'flex') listDriveFiles();
};

function initGoogleAuth() {
    tokenClient = google.accounts.oauth2.initTokenClient({
        client_id: CLIENT_ID,
        scope: 'https://www.googleapis.com/auth/drive.file',
        callback: (res) => {
            accessToken = res.access_token;
            document.getElementById('drive-status').innerText = "On";
            document.getElementById('drive-status').style.color = "#0f0";
            listDriveFiles();
        },
    });
}
document.getElementById('connect-drive').onclick = () => tokenClient.requestAccessToken({ prompt: 'consent' });
window.onload = () => { if (typeof google !== 'undefined') initGoogleAuth(); };
function sendKey(key) {
    const codes = { 'Tab': '\t', 'Escape': '\x1b', 'ArrowUp': '\x1b[A', 'ArrowDown': '\x1b[B', 'ArrowLeft': '\x1b[D', 'ArrowRight': '\x1b[C' };
    if (codes[key]) for(let i=0; i<codes[key].length; i++) emulator.serial0_send(codes[key].charCodeAt(i));
}
