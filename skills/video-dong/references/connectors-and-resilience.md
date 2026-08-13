# วีดีโด่ง — Connectors, Internet และ Resilience

ใช้คู่มือนี้เมื่อ job ต้องอ่านข้อมูลจากอินเทอร์เน็ต เชื่อม Google Drive, GitHub, แอป/API/MCP หรือเรียกเครื่องมือประมวลผลภายนอก จุดประสงค์คือทำให้การเชื่อมต่อ **ตรวจสอบได้ ปลอดภัย ทำซ้ำได้ และหยุดอย่างปลอดภัยเมื่อสถานะไม่แน่นอน**

## 1. ชั้นการเชื่อมต่อ

| ชั้น | ตัวอย่าง | วิธีตรวจ | นโยบาย fallback |
|---|---|---|---|
| แหล่งข้อมูล | เว็บข่าว, RSS, GitHub, API, ไฟล์ผู้ใช้ | URL provenance, license, content type, hash, timestamp | ใช้ source ที่ผ่าน allowlist หรือหยุดเพื่อขอแหล่งใหม่ |
| ที่เก็บข้อมูล | Google Drive ผ่าน `gws`, local job root | auth แบบ read-only ก่อน, file ID, quota, parent folder, hash | เก็บ local manifest และไม่ลบต้นฉบับ |
| แอป/API/MCP | TTS, Avatar, image-to-video, caption, storage | connector manifest, schema, health check, scope, status API | สลับเส้นทางที่ผู้ใช้อนุมัติ หรือหยุดก่อนส่งข้อมูล |
| เครื่องมือประมวลผล | Python, FFmpeg, FFprobe, GitHub/self-hosted | executable/version/license/GPU check | ลดคุณภาพหรือใช้เครื่องมือสำรองที่ระบุไว้ |
| การส่งมอบ | final video, report, logs | เปิดอ่านจริง, hash, size, provenance | เก็บผลลัพธ์และห้าม cleanup จนกว่าจะยืนยันได้ |

ทักษ์ไม่ควรถือว่าแอปหรือ connector ใดมีอยู่เพียงเพราะมีชื่อในเอกสาร ต้องตรวจว่ามี executable/connector ที่ authenticate แล้วจริง และต้องไม่สร้างหรือเผยแพร่ credential เองโดยไม่มีคำสั่งจากผู้ใช้

## 2. Connection manifest

สร้าง `connection-manifest.json` ต่อ job เมื่อมีการเชื่อมต่อภายนอก:

```json
{
  "schema_version": "1.0",
  "job_id": "job-2026-001",
  "display_name": "วีดีโด่ง",
  "connections": [
    {
      "id": "drive-assets",
      "kind": "storage",
      "provider": "google-drive",
      "transport": "gws-cli",
      "purpose": "store frame references and final artifacts",
      "scope": "read-write job folder only",
      "health": "pass",
      "timeout_seconds": 30,
      "read_attempts": 3,
      "mutation_retry": "disabled-unless-idempotent",
      "data_classification": "user-provided-media",
      "last_checked_at": "2026-08-14T00:00:00Z"
    }
  ]
}
```

ห้ามใส่ access token, refresh token, cookie, API key หรือ query string ที่มี secret ลงใน manifest, log, report หรือชื่อไฟล์

## 3. Internet-source policy

ก่อนดาวน์โหลดหรือใช้ข้อมูลจากอินเทอร์เน็ต ให้บันทึก URL ต้นทาง ชื่อผู้เผยแพร่ เวลาเข้าถึง ใบอนุญาต/ข้อกำหนดการใช้งาน content type ขนาด และ SHA-256 หากตรวจใบอนุญาตไม่ได้ ให้ใช้เพื่อการอ้างอิงเท่านั้นและหยุดก่อนนำ asset ไปสร้างวิดีโอ

ให้ใช้ HTTPS เป็นค่าเริ่มต้น ปฏิเสธ URL ที่เป็น `file:`, `data:`, `javascript:`, `ftp:` หรือ URL ที่ resolve ไปยัง loopback, private, link-local, multicast, reserved หรือ unspecified IP เพื่อป้องกัน SSRF จำกัด redirect และขนาดดาวน์โหลด ตรวจ MIME จริงหลังดาวน์โหลด และอย่ารันไฟล์หรือคำสั่งที่มาจากหน้าเว็บโดยอัตโนมัติ

สำหรับข่าว ให้แยก `reported`, `confirmed`, `alleged` และ `unknown` ออกจากกัน บันทึกอย่างน้อยสองแหล่งเมื่อเป็นข้อกล่าวหาหรือข่าวอาชญากรรม และห้ามใช้ภาพ stock/AI ที่ทำให้ผู้ชมเข้าใจว่าเป็นภาพเหตุการณ์จริงโดยไม่ติดป้ายกำกับ

## 4. Retry และสถานะไม่แน่นอน

ใช้ timeout ทุก subprocess และ request การอ่านแบบ idempotent อาจ retry ได้ด้วย exponential backoff และ jitter เช่น 1, 2, 4 วินาที จำกัดจำนวนครั้งและหยุดเมื่อพบ authentication/permission/schema error การสร้างโฟลเดอร์ อัปโหลดไฟล์ ย้ายไฟล์ หรือลบไฟล์ **ห้าม retry อัตโนมัติหลัง timeout** เว้นแต่มี idempotency key หรือค้นหาและยืนยันผลลัพธ์เดิมก่อน เพราะคำขออาจสำเร็จแล้วแต่ response สูญหาย

สถานะที่ต้องบันทึกแยกกันคือ `not_started`, `submitted`, `running`, `succeeded`, `failed`, `unknown_after_timeout`, `verified` และ `quarantined` หากสถานะเป็น `unknown_after_timeout` ให้หยุด cleanup และให้ผู้ใช้ตรวจสอบ provider หรือ file ID ก่อนส่งซ้ำ

## 5. Application/API/MCP adapters

ให้แยก adapter เป็นสี่การดำเนินการ: `submit`, `poll/status`, `download`, `verify`, และ `record` โดยแต่ละ adapterต้องระบุ input/output schema, provider job ID, idempotency key, timeout, retry policy, rate limit, data retention, webhook signature (ถ้ามี) และวิธีปิดงาน

ห้ามส่งภาพใบหน้า เสียง หรือข่าวที่มีข้อมูลส่วนบุคคลไปยัง provider ใหม่โดยไม่แจ้งผู้ใช้และตรวจ consent/data policy ก่อน หาก connector ไม่พร้อม ให้เสนอทางเลือก self-hosted หรือสร้าง preview local แทน ไม่ควร fallback ไปบริการอื่นโดยเงียบ ๆ เพราะอาจเปลี่ยนสิทธิ์และนโยบายข้อมูล

## 6. Google Drive

ใช้ `gws` schema ที่ตรวจสอบได้ก่อนเรียกคำสั่งจริง ทำ health check แบบอ่านอย่างเดียวก่อนอัปโหลด ตรวจ `fileId`, parent, MIME, size และ hash หลังอัปโหลด ใช้โฟลเดอร์ job แยกจากพื้นที่ทั่วไป และไม่ทำให้ไฟล์เป็น public โดยไม่จำเป็น การย้ายไปถังขยะต้องเกิดหลัง final video, manifest และ quality report เปิดอ่านได้จริงและผ่านทุก gate เท่านั้น

## 7. Gap checklist ที่ต้องปิดก่อน production

- มี `scripts/preflight_integrations.py` ตรวจ executable, auth, Drive read-only health, GitHub auth และ HTTPS ตามคำขอ
- มี connection manifest ระบุ provider, scope, classification, health, timeout และ retry policy
- มี structured JSON report และ redaction ของ secret
- มี bounded timeout/retry สำหรับการอ่าน และ no-auto-retry สำหรับ mutation ที่ไม่ idempotent
- มี allowlist/SSRF checks ก่อนเข้าถึง URL
- มี disk-space และ output-hash checks ก่อน cleanup
- มี recovery log และสถานะ `unknown_after_timeout`
- มี dry-run เป็นค่าเริ่มต้นสำหรับการเปลี่ยนแปลงที่ทำลายข้อมูล
- มี human/semantic review แยกจาก machine gates โดยเฉพาะ identity, ข่าว และความถูกต้องของบริบท
