/**
 * Drive Terminal AI Edition - app.js
 */

const CLIENT_ID = 'YOUR_GOOGLE_CLIENT_ID.apps.googleusercontent.com';
const SCOPES = 'https://www.googleapis.com/auth/drive.file';

let accessToken = null;
let tokenClient;

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

// 3. AI Helper Logic (Mocked Gemini Interface)
document.getElementById('ai-ask-btn').onclick = async () => {
    const query = document.getElementById('ai-input').value;
    if (!query) return;
    
    document.getElementById('ai-text').textContent = "กำลังวิเคราะห์คำสั่งด้วย AI...";
    document.getElementById('ai-code').textContent = "";
    document.getElementById('ai-response-overlay').style.display = 'block';

    // ในสถานการณ์จริง จะส่งคำสั่งไปที่ API ของ Gemini
    // นี่คือตัวอย่างการจำลองการตอบกลับของ AI
    setTimeout(() => {
        let responseText = "";
        let command = "";

        if (query.includes("Python") || query.includes("ไพทอน")) {
            responseText = "ในการติดตั้ง Python 3 บนระบบ Alpine Linux ให้ใช้คำสั่งต่อไปนี้:";
            command = "apk update && apk add python3";
        } else if (query.includes("Git") || query.includes("กิต")) {
            responseText = "ในการติดตั้ง Git เพื่อโคลนโค้ด ให้ใช้คำสั่ง:";
            command = "apk add git";
        } else {
            responseText = "ฉันขอแนะนำให้คุณเริ่มด้วยการอัปเดตแพ็กเกจระบบ:";
            command = "apk update";
        }

        document.getElementById('ai-text').textContent = responseText;
        document.getElementById('ai-code').textContent = command;
    }, 1000);
};

document.getElementById('run-ai-code').onclick = () => {
    const code = document.getElementById('ai-code').textContent;
    if (code) {
        for(let i=0; i<code.length; i++) emulator.serial0_send(code.charCodeAt(i));
        emulator.serial0_send(13); // ส่ง Enter
        document.getElementById('ai-response-overlay').style.display = 'none';
    }
};

document.getElementById('close-ai').onclick = () => {
    document.getElementById('ai-response-overlay').style.display = 'none';
};

// 4. Standard Functions
function initGoogleAuth() {
    tokenClient = google.accounts.oauth2.initTokenClient({
        client_id: CLIENT_ID,
        scope: 'https://www.googleapis.com/auth/drive.file',
        callback: (res) => {
            accessToken = res.access_token;
            document.getElementById('drive-status').innerText = "AI-Connected";
            document.getElementById('drive-status').style.color = "#0f0";
        },
    });
}
document.getElementById('connect-drive').onclick = () => tokenClient.requestAccessToken({ prompt: 'consent' });
window.onload = () => { if (typeof google !== 'undefined') initGoogleAuth(); };
function sendKey(key) {
    const codes = { 'Tab': '\t', 'Escape': '\x1b', 'ArrowUp': '\x1b[A', 'ArrowDown': '\x1b[B', 'ArrowLeft': '\x1b[D', 'ArrowRight': '\x1b[C' };
    if (codes[key]) for(let i=0; i<codes[key].length; i++) emulator.serial0_send(codes[key].charCodeAt(i));
}
