/**
 * Drive Terminal Ultra - app.js
 * Advanced CLI Drive Management & Package Persistence
 */

const CLIENT_ID = 'YOUR_GOOGLE_CLIENT_ID.apps.googleusercontent.com';
const SCOPES = 'https://www.googleapis.com/auth/drive.file https://www.googleapis.com/auth/drive.metadata.readonly https://www.googleapis.com/auth/drive.readonly';
const STATE_FILENAME = 'drive_terminal_ultra_state.bin';

let accessToken = null;
let tokenClient;
let currentStateFileId = null;

// 1. Terminal Setup
const term = new Terminal({ cursorBlink: true, fontSize: 14, theme: { background: '#000', foreground: '#0f0' } });
const fitAddon = new FitAddon.FitAddon();
term.loadAddon(fitAddon);
term.open(document.getElementById('terminal-container'));
fitAddon.fit();

term.writeln('\x1b[1;35m[Drive Terminal Ultra Edition]\x1b[0m');
term.writeln('System Ready. Package Manager: apk (Alpine Linux)');
term.writeln('Drive CLI commands enabled: drive-ls, drive-push, drive-pull');

// 2. Emulator Setup (512MB RAM, Network Enabled)
let emulator = new V86Starter({
    wasm_path: "https://copy.sh/v86/v86.wasm",
    memory_size: 512 * 1024 * 1024,
    vga_memory_size: 2 * 1024 * 1024,
    screen_container: document.getElementById('screen-container'),
    bios: { url: "https://copy.sh/v86/bios/seabios.bin" },
    vga_bios: { url: "https://copy.sh/v86/bios/vgabios.bin" },
    cdrom: { url: "https://copy.sh/v86/images/alpine.iso" },
    network_relay_url: "wss://relay.widgetry.org/",
    autostart: true,
});

emulator.add_listener("serial0-output-char", (char) => term.write(char));
term.onData(data => { for(let i=0; i<data.length; i++) emulator.serial0_send(data.charCodeAt(i)); });

// 3. Ultra Drive CLI Implementation
// ฟังก์ชันสำหรับส่งคำสั่งจำลองเข้าไปใน Terminal
function systemMessage(msg) {
    term.writeln('\r\n\x1b[1;33m[Ultra-Drive]\x1b[0m ' + msg);
}

async function driveList() {
    if (!accessToken) return systemMessage("Error: Login required.");
    systemMessage("Fetching files from Google Drive...");
    const res = await fetch('https://www.googleapis.com/drive/v3/files?pageSize=50&fields=files(id, name, mimeType)', {
        headers: { 'Authorization': `Bearer ${accessToken}` }
    });
    const data = await res.json();
    term.writeln('\r\nID\t\t\t\tNAME\t\t\tTYPE');
    term.writeln('----------------------------------------------------------------------');
    data.files.forEach(f => {
        term.writeln(`${f.id.substring(0,8)}...\t${f.name}\t[${f.mimeType.split('.').pop()}]`);
    });
}

// 4. Persistence & Sync
async function saveUltraState() {
    if (!accessToken) return alert("Login to Drive first");
    systemMessage("Capturing system state and installed libraries...");
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
        systemMessage("All tools and libraries synced to Google Drive!");
    });
}

// 5. Auth & UI
function initGoogleAuth() {
    tokenClient = google.accounts.oauth2.initTokenClient({
        client_id: CLIENT_ID,
        scope: SCOPES,
        callback: (res) => {
            accessToken = res.access_token;
            document.getElementById('drive-status').innerText = "Ultra-Connected";
            document.getElementById('drive-status').style.color = "#0f0";
            systemMessage("Google Drive API Authenticated.");
        },
    });
}

document.getElementById('connect-drive').onclick = () => tokenClient.requestAccessToken({ prompt: 'consent' });
window.onload = () => { if (typeof google !== 'undefined') initGoogleAuth(); };
window.syncToDrive = saveUltraState;

// Mobile Keys & Commands
function sendKey(key) {
    const codes = { 'Tab': '\t', 'Escape': '\x1b', 'ArrowUp': '\x1b[A', 'ArrowDown': '\x1b[B', 'ArrowLeft': '\x1b[D', 'ArrowRight': '\x1b[C' };
    if (codes[key]) for(let i=0; i<codes[key].length; i++) emulator.serial0_send(codes[key].charCodeAt(i));
}

// เพิ่มปุ่มสำหรับคำสั่ง Drive พิเศษ
document.getElementById('toggle-explorer').innerText = "DRIVE-LS";
document.getElementById('toggle-explorer').onclick = driveList;
