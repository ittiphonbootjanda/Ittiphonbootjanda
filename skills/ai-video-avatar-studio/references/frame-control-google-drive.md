# First/Last-Frame Control กับ Google Drive

สคริปต์ `scripts/sync_frame_controls_to_drive.py` เชื่อมภาพเฟรมแรกและเฟรมสุดท้ายของแต่ละฉากเข้ากับ Google Drive ผ่านคำสั่ง `gws drive files ...` โดยสร้าง manifest ที่ downstream render pipeline ใช้เป็น scene anchor ได้ สคริปต์นี้ไม่ลบและไม่ย้ายไฟล์ไปถังขยะ เพื่อป้องกันการลบ reference ก่อน final video ผ่าน quality gate

> **หลักการ:** first frame เป็นจุดเริ่มต้นของฉาก ส่วน last frame เป็นจุดจบและเป็น anchor สำหรับฉากถัดไป เมื่อเครื่องมือสร้างวิดีโอรองรับการใช้ภาพอ้างอิงหรือการต่อฉาก

## ข้อมูลที่สคริปต์บันทึก

| ส่วน | ข้อมูล |
|---|---|
| Job identity | `job_id`, `scene_id`, เวลา UTC และ schema version |
| Frame provenance | path ต้นทาง, Drive file ID, ชื่อไฟล์, MIME type และลิงก์ |
| Integrity | SHA-256 ของไฟล์ local, ขนาดไฟล์, width, height และ format |
| Continuity | การใช้ first frame เป็น scene anchor และ last frame เป็น next-scene anchor |
| Identity | `preserve_exact_person`, ปิด face swap และปิด identity drift |
| Cleanup | ระบุชัดว่าสคริปต์ไม่ทำ trash/delete |

## การติดตั้งและข้อกำหนด

ต้องมี Python 3.10 ขึ้นไป, Pillow และ `gws` CLI ที่ผ่านการ authenticate กับ Google Drive แล้ว หากใช้เฉพาะ `--dry-run` จะไม่เรียก Google Drive และใช้ตรวจสอบภาพ local ได้โดยไม่แตะข้อมูลบนคลาวด์

```bash
sudo pip3 install pillow
chmod +x scripts/sync_frame_controls_to_drive.py
```

## โหมด dry-run

ใช้ตรวจภาพและสร้าง manifest โดยไม่อัปโหลด:

```bash
python3 scripts/sync_frame_controls_to_drive.py \
  --job-id job-2026-001 \
  --scene-id scene-001 \
  --first-frame ./frames/scene-001-first.png \
  --last-frame ./frames/scene-001-last.png \
  --manifest-out ./job-2026-001/scene-001-frame-control.json \
  --dry-run
```

สคริปต์จะตรวจว่าไฟล์มีอยู่จริง เป็น PNG/JPEG/WebP อ่านได้ และมีขนาดอย่างน้อย 2×2 พิกเซล จากนั้นคำนวณ SHA-256 และบันทึกสถานะ `dry_run`

## โหมดอัปโหลดเข้าโฟลเดอร์ Drive ที่มีอยู่แล้ว

```bash
python3 scripts/sync_frame_controls_to_drive.py \
  --job-id job-2026-001 \
  --scene-id scene-001 \
  --folder-id DRIVE_JOB_FOLDER_ID \
  --first-frame ./frames/scene-001-first.png \
  --last-frame ./frames/scene-001-last.png \
  --manifest-out ./job-2026-001/scene-001-frame-control.json
```

สคริปต์จะอัปโหลดภาพเข้าโฟลเดอร์ที่ระบุ อ่าน metadata กลับจาก Drive และตรวจขนาดไฟล์กับ local source ก่อนเขียนสถานะ `verified` ลง manifest หาก Drive file ถูกย้ายไปถังขยะ หรือ metadata ไม่ตรงกับต้นฉบับ สคริปต์จะหยุดและคืนค่า error

## โหมดสร้างโฟลเดอร์ใหม่

```bash
python3 scripts/sync_frame_controls_to_drive.py \
  --job-id job-2026-001 \
  --scene-id scene-001 \
  --create-folder \
  --folder-name job-2026-001-frames \
  --parent-folder-id DRIVE_PARENT_FOLDER_ID \
  --first-frame ./frames/scene-001-first.png \
  --last-frame ./frames/scene-001-last.png
```

หากไม่ระบุ `--parent-folder-id` โฟลเดอร์จะถูกสร้างในตำแหน่งเริ่มต้นของ Drive ตามสิทธิ์ของบัญชีที่ authenticate ไว้ ควรใช้โฟลเดอร์ job ที่กำหนดไว้ล่วงหน้าใน production เพื่อให้ง่ายต่อการติดตาม provenance และ cleanup ภายหลัง

## โหมดอ้างอิงไฟล์ที่อยู่บน Drive แล้ว

ถ้าไฟล์ถูกอัปโหลดโดยขั้นตอนอื่น ให้ใช้ file ID แทนการอัปโหลดซ้ำ:

```bash
python3 scripts/sync_frame_controls_to_drive.py \
  --job-id job-2026-001 \
  --scene-id scene-001 \
  --first-frame-file-id DRIVE_FIRST_FRAME_ID \
  --last-frame-file-id DRIVE_LAST_FRAME_ID \
  --manifest-out ./job-2026-001/scene-001-frame-control.json
```

ก่อนลงทะเบียน สคริปต์จะอ่าน metadata ของไฟล์ผ่าน Drive และปฏิเสธไฟล์ที่ถูก trash หรือมี MIME type ไม่ใช่ภาพที่รองรับ

## การส่งต่อเข้า render pipeline

ให้ใช้ค่าต่อไปนี้จาก manifest:

```json
{
  "frames": {
    "first": {"drive_file_id": "...", "web_view_link": "..."},
    "last": {"drive_file_id": "...", "web_view_link": "..."}
  },
  "continuity_policy": {
    "use_first_frame_as_scene_anchor": true,
    "use_last_frame_as_next_scene_anchor": true,
    "preserve_exact_person": true,
    "allow_face_swap": false,
    "allow_identity_drift": false
  }
}
```

Adapter ของ provider วิดีโอควรแปลง `drive_file_id` เป็นไฟล์ local หรือ signed input ตามข้อกำหนดของ provider โดยไม่ทำให้ไฟล์ Drive เป็น public โดยไม่จำเป็น และควรเก็บ provider request ID, model/version, prompt hash และ output hash กลับเข้า provenance

## ข้อจำกัดและ quality gate

สคริปต์นี้จัดการ **การอ้างอิงและ provenance ของเฟรม** ไม่ได้สร้างวิดีโอและไม่รับประกันว่า provider จะรักษาความเหมือนของบุคคลได้เอง ก่อนใช้ผลลัพธ์เป็น final ให้ตรวจ identity preservation, prompt adherence, continuity, frame rate, duration, audio sync และความถูกต้องของ first/last frame ตาม [render-pipeline.md](render-pipeline.md) และ [veo-inspired-video.md](veo-inspired-video.md)

ห้ามเรียกใช้สคริปต์นี้เพื่อย้ายหรือลบภาพต้นฉบับ และห้ามทำ cleanup จนกว่าวิดีโอ final, manifest และ quality report จะถูกบันทึกใน Google Drive และผ่าน gate ครบทุกข้อ ตามแนวทาง [google-drive-cleanup.md](google-drive-cleanup.md)
