# วีดีโด่ง — Integration Audit

วันที่ตรวจ: 2026-08-13 UTC

## ผลตรวจสภาพแวดล้อม

- `gws` พร้อมใช้งานที่ `/home/ubuntu/.local/share/pnpm/bin/gws`
- Google Drive schema `drive.about.get` ตรวจสอบได้ และรองรับข้อมูลผู้ใช้/โควตา/ความสามารถการอัปโหลดตาม schema ที่คืนมา
- `gh` พร้อมใช้งาน และบัญชี GitHub `ittiphonbootjanda` authenticated สำหรับ repository ที่เลือก
- `ffmpeg`, `ffprobe`, `python3` และ `curl` พร้อมใช้งาน
- HTTPS outbound ใช้งานได้ โดยทดสอบ `https://www.google.com` ได้ HTTP 200
- `manus-config config load --search 'drive\\|github\\|browser\\|api\\|mcp'` ไม่พบ connector match ใน `config.json`; การเชื่อม Google Drive/GitHub ที่ทำงานได้มาจาก CLI integration ที่ติดตั้งไว้ ไม่ควรเดาหรือสร้าง credential ใหม่เอง

## ช่องว่างที่พบจากการตรวจทักษ์

1. การเรียก `gws` ใน frame-control ใช้ `subprocess.run` โดยไม่มี timeout, retry แบบ exponential backoff, จำกัด output หรือการตรวจ idempotency
2. การอัปโหลด local frame ยังไม่มีการค้นหาไฟล์เดิมตาม job/scene/hash เพื่อป้องกัน duplicate upload เมื่อ retry
3. ยังไม่มี preflight script กลางสำหรับตรวจเครื่องมือ, authentication, Drive quota, GitHub auth และ HTTPS ก่อนเริ่มงาน
4. ยังไม่มี connection manifest ที่ระบุ provider, scope, data classification, endpoint, timeout, retry policy, health-check และ fallback
5. ยังไม่มี internet-source adapter ที่บังคับ allowlist, URL provenance, license/status, content hash และการป้องกัน SSRF/redirect ไป private IP
6. คู่มือยังกล่าวถึง API/self-hosted/GitHub แต่ยังไม่มี contract กลางสำหรับ `submit`, `poll`, `download`, `verify`, `record` และ idempotency key
7. ชื่อใน frontmatter ยังเป็น `ai-video-avatar-studio`; ต้องเพิ่มชื่อแสดงผลภาษาไทย `วีดีโด่ง` และ technical id `video-dong` โดยคง compatibility alias
8. ต้องเพิ่ม resilience controls ได้แก่ timeout, bounded retry, jitter, circuit-breaker-like stop, structured logs, redaction ของ token/URL query secrets, disk-space check และ recovery state

## ข้อจำกัดด้านความปลอดภัย

ห้ามพิมพ์ token หรือ credential ลง log, ห้ามทำให้ไฟล์ Drive เป็น public โดยไม่จำเป็น, ห้ามดาวน์โหลดหรือประมวลผล URL ที่ไม่ผ่าน policy, ห้ามลบต้นฉบับก่อน final quality gate และควรใช้ dry-run เป็นค่าเริ่มต้นสำหรับ cleanup/connector mutation
