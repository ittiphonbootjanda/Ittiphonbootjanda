/**
 * Drive Terminal Auto-Protect Edition - app.js
 */

const CLIENT_ID = 'YOUR_GOOGLE_CLIENT_ID.apps.googleusercontent.com';
const SCOPES = 'https://www.googleapis.com/auth/drive.file';
const STATE_FILENAME = 'drive_terminal_autosafe_state.bin';

let accessToken = null;
let tokenClient;
let currentStateFileId = null;
let isSyncing = false;

// 1. Terminal & Emulator Setup (Same as Creator Edition)
const term = new Terminal({ cursorBlink: true, fontSize: 14, theme: { background: '#000', foreground: '#0f0' } });
const fitAddon = new FitAddon.FitAddon();
term.loadAddon(fitAddon);
term.open(document.getElementById('terminal-container'));
fitAddon.fit();

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

// 2. Enhanced Auto-Sync Logic
async function autoSave() {
    if (!accessToken || isSyncing) return;
    isSyncing = true;
    
    console.log("[Auto-Save] Triggered...");
    term.write('\r\n\x1b[1;33m[Auto-Protect] Saving state to Drive...\x1b[0m\r\n');

    emulator.save_state(async (err, state) => {
        if (err) {
            isSyncing = false;
            return console.error(err);
        }

        const metadata = { name: STATE_FILENAME, mimeType: 'application/octet-stream' };
        const file = new Blob([state], { type: 'application/octet-stream' });
        const formData = new FormData();
        formData.append('metadata', new Blob([JSON.stringify(metadata)], { type: 'application/json' }));
        formData.append('file', file);

        const url = currentStateFileId ? `https://www.googleapis.com/upload/drive/v3/files/${currentStateFileId}?uploadType=multipart` : 'https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart';
        const method = currentStateFileId ? 'PATCH' : 'POST';

        try {
            const res = await fetch(url, { method, headers: { 'Authorization': `Bearer ${accessToken}` }, body: formData });
            const result = await res.json();
            currentStateFileId = result.id;
            term.write('\x1b[1;32m[Auto-Protect] Sync Complete!\x1b[0m\r\n');
        } catch (err) {
            console.error("Auto-save failed", err);
        } finally {
            isSyncing = false;
        }
    });
}

// 3. Event Listeners for Auto-Sync
// A. บันทึกเมื่อสลับแอป หรือย่อหน้าจอ (เสถียรที่สุดบนมือถือ)
document.addEventListener('visibilitychange', () => {
    if (document.visibilityState === 'hidden') {
        autoSave();
    }
});

// B. บันทึกทุกๆ 10 นาที (ป้องกันเครื่องค้าง)
setInterval(autoSave, 10 * 60 * 1000);

// C. พยายามบันทึกเมื่อปิดหน้าต่าง (อาจไม่สำเร็จในบางเบราว์เซอร์ แต่ใส่ไว้เพื่อความชัวร์)
window.addEventListener('beforeunload', (event) => {
    if (accessToken) {
        autoSave();
        // แสดงคำเตือนเพื่อให้เบราว์เซอร์มีเวลาประมวลผลการบันทึก
        event.preventDefault();
        event.returnValue = '';
    }
});

// 4. Standard Auth & Sync Functions
async function syncToDrive() { await autoSave(); }

function initGoogleAuth() {
    tokenClient = google.accounts.oauth2.initTokenClient({
        client_id: CLIENT_ID,
        scope: 'https://www.googleapis.com/auth/drive.file',
        callback: (res) => {
            accessToken = res.access_token;
            document.getElementById('drive-status').innerText = "Protected";
            document.getElementById('drive-status').style.color = "#0f0";
            term.writeln('\r\n[System] Auto-Protect Enabled.');
        },
    });
}
document.getElementById('connect-drive').onclick = () => tokenClient.requestAccessToken({ prompt: 'consent' });
window.onload = () => { if (typeof google !== 'undefined') initGoogleAuth(); };
function sendKey(key) {
    const codes = { 'Tab': '\t', 'Escape': '\x1b', 'ArrowUp': '\x1b[A', 'ArrowDown': '\x1b[B', 'ArrowLeft': '\x1b[D', 'ArrowRight': '\x1b[C' };
    if (codes[key]) for(let i=0; i<codes[key].length; i++) emulator.serial0_send(codes[key].charCodeAt(i));
}
