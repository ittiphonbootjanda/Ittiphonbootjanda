/**
 * Drive Terminal Pro Max - app.js
 * Full Networking & Package Management Support
 */

const CLIENT_ID = 'YOUR_GOOGLE_CLIENT_ID.apps.googleusercontent.com';
const SCOPES = 'https://www.googleapis.com/auth/drive.file https://www.googleapis.com/auth/drive.metadata.readonly';
const STATE_FILENAME = 'drive_terminal_promax_state.bin';

let accessToken = null;
let tokenClient;
let currentStateFileId = null;

// 1. Terminal Setup
const term = new Terminal({ cursorBlink: true, fontSize: 14, theme: { background: '#000', foreground: '#0f0' } });
const fitAddon = new FitAddon.FitAddon();
term.loadAddon(fitAddon);
term.open(document.getElementById('terminal-container'));
fitAddon.fit();

term.writeln('\x1b[1;36m[Drive Terminal Pro Max]\x1b[0m');
term.writeln('System Ready. Internet Connection: ENABLED.');
term.writeln('Use "apk add <pkg>" to install tools like in Raspberry Pi.');

// 2. Emulator Setup with Networking (v86)
let emulator = new V86Starter({
    wasm_path: "https://copy.sh/v86/v86.wasm",
    memory_size: 512 * 1024 * 1024, // เพิ่มเป็น 512MB เพื่อรองรับการคอมไพล์โค้ด
    vga_memory_size: 2 * 1024 * 1024,
    screen_container: document.getElementById('screen-container'),
    bios: { url: "https://copy.sh/v86/bios/seabios.bin" },
    vga_bios: { url: "https://copy.sh/v86/bios/vgabios.bin" },
    cdrom: { url: "https://copy.sh/v86/images/alpine.iso" },
    network_relay_url: "wss://relay.widgetry.org/", // เปิดระบบอินเทอร์เน็ตผ่าน Relay
    autostart: true,
});

emulator.add_listener("serial0-output-char", (char) => term.write(char));
term.onData(data => { for(let i=0; i<data.length; i++) emulator.serial0_send(data.charCodeAt(i)); });

// 3. Drive Sync & Explorer Logic (Same as Pro/Explorer)
async function listDriveFiles() {
    if (!accessToken) return;
    try {
        const response = await fetch('https://www.googleapis.com/drive/v3/files?pageSize=20&fields=files(id, name, mimeType)', {
            headers: { 'Authorization': `Bearer ${accessToken}` }
        });
        const data = await response.json();
        const fileList = document.getElementById('file-list');
        fileList.innerHTML = '';
        if (data.files) {
            data.files.forEach(file => {
                const li = document.createElement('li');
                li.textContent = (file.mimeType.includes('folder') ? '📁 ' : '📄 ') + file.name;
                li.onclick = () => { if(file.name === STATE_FILENAME) loadStateFromDrive(file.id); };
                fileList.appendChild(li);
                if (file.name === STATE_FILENAME) currentStateFileId = file.id;
            });
        }
    } catch (err) { console.error(err); }
}

async function loadStateFromDrive(fileId) {
    term.writeln('\r\n[System] Restoring Pro Max Environment...');
    const response = await fetch(`https://www.googleapis.com/drive/v3/files/${fileId}?alt=media`, {
        headers: { 'Authorization': `Bearer ${accessToken}` }
    });
    const buffer = await (await response.blob()).arrayBuffer();
    emulator.restore_state(buffer);
    term.writeln('[System] Environment Restored. Internet Ready.');
}

async function saveStateToDrive() {
    if (!accessToken) return alert("Login to Drive first");
    term.writeln('\r\n[System] Saving entire environment (RAM + State)...');
    emulator.save_state(async (err, state) => {
        if (err) return term.writeln('[Error] ' + err);
        const metadata = { name: STATE_FILENAME, mimeType: 'application/octet-stream' };
        const file = new Blob([state], { type: 'application/octet-stream' });
        const formData = new FormData();
        formData.append('metadata', new Blob([JSON.stringify(metadata)], { type: 'application/json' }));
        formData.append('file', file);
        const url = currentStateFileId ? `https://www.googleapis.com/upload/drive/v3/files/${currentStateFileId}?uploadType=multipart` : 'https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart';
        const method = currentStateFileId ? 'PATCH' : 'POST';
        const res = await fetch(url, { method, headers: { 'Authorization': `Bearer ${accessToken}` }, body: formData });
        const result = await res.json();
        currentStateFileId = result.id;
        term.writeln('[System] Full Sync Complete!');
        listDriveFiles();
    });
}

// 4. UI & Auth
document.getElementById('toggle-explorer').onclick = () => {
    const explorer = document.getElementById('drive-explorer');
    explorer.style.display = explorer.style.display === 'flex' ? 'none' : 'flex';
    if (explorer.style.display === 'flex') listDriveFiles();
};

function initGoogleAuth() {
    tokenClient = google.accounts.oauth2.initTokenClient({
        client_id: CLIENT_ID,
        scope: SCOPES,
        callback: (res) => {
            accessToken = res.access_token;
            document.getElementById('drive-status').innerText = "Connected";
            document.getElementById('drive-status').style.color = "#0f0";
            listDriveFiles();
        },
    });
}

document.getElementById('connect-drive').onclick = () => tokenClient.requestAccessToken({ prompt: 'consent' });
window.onload = () => { if (typeof google !== 'undefined') initGoogleAuth(); };
window.syncToDrive = saveStateToDrive;
function sendKey(key) {
    const codes = { 'Tab': '\t', 'Escape': '\x1b', 'ArrowUp': '\x1b[A', 'ArrowDown': '\x1b[B', 'ArrowLeft': '\x1b[D', 'ArrowRight': '\x1b[C' };
    if (codes[key]) for(let i=0; i<codes[key].length; i++) emulator.serial0_send(codes[key].charCodeAt(i));
}
