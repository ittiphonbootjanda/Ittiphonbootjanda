# Drive Terminal (Termux for Web & Google Drive)

แอปพลิเคชัน Terminal ที่ทำงานบนเบราว์เซอร์มือถือโดยใช้พลังประมวลผลจากเครื่องของคุณเอง (WebAssembly) และสามารถเชื่อมต่อกับ Google Drive เพื่อเก็บข้อมูลได้

## คุณสมบัติหลัก
- **WASM-Powered Linux Sandbox:** รันระบบปฏิบัติการ Linux จริงๆ บนเบราว์เซอร์ ไม่ต้องมีเซิร์ฟเวอร์
- **Mobile Friendly:** มีแถบเครื่องมือสำหรับคีย์พิเศษ (Tab, Ctrl, Alt, ลูกศร) ที่ใช้งานง่ายบนมือถือ
- **Google Drive Storage:** ออกแบบมาเพื่อเชื่อมต่อกับพื้นที่เก็บข้อมูลของคุณเอง
- **Serverless:** ทำงานได้ทันทีเพียงแค่เปิดไฟล์ HTML

## วิธีการใช้งาน
1. ดาวน์โหลดไฟล์ `index.html` และ `app.js` ไปไว้ใน Google Drive ของคุณ
2. ใช้บริการอย่าง [GitHub Pages](https://pages.github.com/) หรือ [Vercel](https://vercel.com/) เพื่อโฮสต์ไฟล์เหล่านี้ (หรือเปิดผ่านเครื่องมืออย่าง Web Server บนมือถือ)
3. เมื่อเปิดแอป ระบบจะทำการโหลด Linux Kernel ผ่าน WebAssembly
4. คุณสามารถพิมพ์คำสั่ง Linux พื้นฐานได้ทันที

## การเชื่อมต่อ Google Drive (สำหรับผู้พัฒนา/ผู้ใช้ขั้นสูง)
หากต้องการให้ระบบบันทึกข้อมูลลง Drive จริงๆ คุณต้อง:
1. ไปที่ [Google Cloud Console](https://console.cloud.google.com/)
2. สร้างโปรเจกต์ใหม่และเปิดใช้งาน **Google Drive API**
3. สร้าง **OAuth 2.0 Client ID** (เลือกประเภท Web Application)
4. นำ Client ID มาใส่ในไฟล์ `app.js` ในส่วนการตั้งค่า Google Drive

---
*หมายเหตุ: โปรแกรมนี้เป็น Sandbox ที่รันบนหน่วยความจำของเบราว์เซอร์ หากรีเฟรชหน้าเว็บโดยไม่ได้เชื่อมต่อระบบ Sync ข้อมูลอาจจะหายไป*
