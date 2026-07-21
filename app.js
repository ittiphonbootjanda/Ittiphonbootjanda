/**
 * Drive Terminal Gemini Bridge Edition - app.js
 */

const CLIENT_ID = 'YOUR_GOOGLE_CLIENT_ID.apps.googleusercontent.com';
const GEMINI_FOLDER_NAME = 'DriveTerminal_Gemini';

let accessToken = null;
let tokenClient;
let geminiFolderId = null;

// 1. Terminal Setup
const term = new Terminal({ cursorBlink: true, fontSize: 14, theme: { background: '#000', foreground: '#0f0' } });
const fitAddon = new FitAddon.FitAddon();
term.loadAddon(fitAddon);
term.open(document.getElementById('terminal-container'));
fitAddon.fit();

term.writeln('\x1b[1;34m[Gemini Bridge Edition Ready]\x1b[0m');
term.writeln('Listening for commands from Gemini via Google Drive...');

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

// 3. Gemini Bridge Logic (Auto-Fetch from Drive)
async function findGeminiFolder() {
    const res = await fetch(`https://www.googleapis.com/drive/v3/files?q=name='${GEMINI_FOLDER_NAME}' and mimeType='application/vnd.google-apps.folder' and trashed=false`, {
        headers: { 'Authorization': `Bearer ${accessToken}` }
    });
    const data = await res.json();
    if (data.files && data.files.length > 0) {
        geminiFolderId = data.files[0].id;
    } else {
        // สร้างโฟลเดอร์ถ้าไม่มี
        const createRes = await fetch('https://www.googleapis.com/drive/v3/files', {
            method: 'POST',
            headers: { 'Authorization': `Bearer ${accessToken}`, 'Content-Type': 'application/json' },
            body: JSON.stringify({ name: GEMINI_FOLDER_NAME, mimeType: 'application/vnd.google-apps.folder' })
        });
        const folder = await createRes.json();
        geminiFolderId = folder.id;
    }
}

async function checkForGeminiCommands() {
    if (!accessToken || !geminiFolderId) return;
    
    // ค้นหาไฟล์ .sh หรือ .txt ล่าสุดในโฟลเดอร์ Gemini
    const res = await fetch(`https://www.googleapis.com/drive/v3/files?q='${geminiFolderId}' in parents and trashed=false&orderBy=createdTime desc&pageSize=1`, {
        headers: { 'Authorization': `Bearer ${accessToken}` }
    });
    const data = await res.json();
    
    if (data.files && data.files.length > 0) {
        const file = data.files[0];
        // ถ้าเป็นไฟล์ใหม่ที่ยังไม่ได้รัน (จำลองโดยใช้ ID)
        if (window.lastCommandId !== file.id) {
            window.lastCommandId = file.id;
            term.writeln(`\r\n\x1b[1;33m[Gemini Bridge] New command received: ${file.name}\x1b[0m`);
            
            const contentRes = await fetch(`https://www.googleapis.com/drive/v3/files/${file.id}?alt=media`, {
                headers: { 'Authorization': `Bearer ${accessToken}` }
            });
            const command = await contentRes.text();
            
            if (confirm(`Run command from Gemini: \n\n${command}`)) {
                for(let i=0; i<command.length; i++) emulator.serial0_send(command.charCodeAt(i));
                emulator.serial0_send(13); // Enter
            }
        }
    }
}

// ตรวจสอบคำสั่งใหม่ทุก 15 วินาที
setInterval(checkForGeminiCommands, 15000);

// 4. Auth
function initGoogleAuth() {
    tokenClient = google.accounts.oauth2.initTokenClient({
        client_id: CLIENT_ID,
        scope: 'https://www.googleapis.com/auth/drive.file',
        callback: async (res) => {
            accessToken = res.access_token;
            document.getElementById('drive-status').innerText = "Bridge-Active";
            document.getElementById('drive-status').style.color = "#0f0";
            await findGeminiFolder();
        },
    });
}
document.getElementById('connect-drive').onclick = () => tokenClient.requestAccessToken({ prompt: 'consent' });
window.onload = () => { if (typeof google !== 'undefined') initGoogleAuth(); };
function sendKey(key) {
    const codes = { 'Tab': '\t', 'Escape': '\x1b', 'ArrowUp': '\x1b[A', 'ArrowDown': '\x1b[B', 'ArrowLeft': '\x1b[D', 'ArrowRight': '\x1b[C' };
    if (codes[key]) for(let i=0; i<codes[key].length; i++) emulator.serial0_send(codes[key].charCodeAt(i));
}
