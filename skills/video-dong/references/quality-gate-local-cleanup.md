# Video Quality Gate และ Local Cleanup

ใช้ `scripts/run_video_quality_gate.py` หลัง export final video และก่อนลบหรือย้ายไฟล์ชั่วคราวในเครื่อง สคริปต์ตรวจ metadata ด้วย `ffprobe`, ถอดรหัสทั้งไฟล์ด้วย `ffmpeg` ตามค่าเริ่มต้น, ตรวจ audio/video timing, ตรวจ captions, ตรวจ semantic gates ที่ประกาศใน manifest, บันทึก SHA-256 ของ final output และเขียน `quality-report.json`

## ลำดับการทำงาน

1. ตรวจว่า final video มีอยู่จริงและมีขนาดมากกว่าศูนย์
2. อ่าน video/audio stream ด้วย `ffprobe`
3. ตรวจ width, height, aspect ratio, fps และ duration ตาม `quality_requirements`
4. ตรวจว่ามี audio/captions เมื่อ manifest กำหนดให้ต้องมี
5. ถอดรหัสทั้งไฟล์ด้วย `ffmpeg` เพื่อจับ frame หรือ packet ที่เสีย
6. ตรวจ semantic review เช่น `identity_status`, `lip_sync_status`, `language_review_status` และ `news_ethics_status` โดยไม่เดาสถานะที่ยังเป็น `pending`
7. สร้าง quality report พร้อม output hash
8. เมื่อ gate ผ่านและ `cleanup.local_cleanup_allowed` เป็น `true` ให้ย้ายเฉพาะไฟล์ใน `cleanup.local_candidate_paths` ไปยัง `.cleanup-trash/<timestamp>/`

## ตัวอย่าง manifest ขั้นต่ำ

```json
{
  "job_id": "av-2026-001",
  "final_video": "final/video.mp4",
  "quality_requirements": {
    "width": 1080,
    "height": 1920,
    "fps": 30,
    "duration_sec": 30,
    "duration_tolerance_sec": 0.35,
    "aspect_ratio": "9:16",
    "audio_required": true,
    "captions_required": true,
    "provenance_required": true,
    "required_semantic_gates": [
      "identity_status",
      "lip_sync_status",
      "language_review_status"
    ]
  },
  "semantic_review": {
    "identity_status": "pass",
    "lip_sync_status": "pass",
    "language_review_status": "pass"
  },
  "provenance_status": "pass",
  "cleanup": {
    "job_root": ".",
    "local_cleanup_allowed": true,
    "local_candidate_paths": [
      "working/render-cache.json",
      "working/preview-low.mp4"
    ]
  }
}
```

## คำสั่งใช้งาน

ตรวจอย่างเดียวและเขียนรายงาน:

```bash
python3 scripts/run_video_quality_gate.py \
  ./job_id/manifest.json \
  --report-out ./job_id/quality-report.json
```

ตรวจและย้ายไฟล์ชั่วคราวไป quarantine หลัง gate ผ่าน:

```bash
python3 scripts/run_video_quality_gate.py \
  ./job_id/manifest.json \
  --report-out ./job_id/quality-report.json \
  --cleanup
```

หากต้องอนุญาตงานที่มีคำเตือน ให้ใช้ `--allow-warnings` เฉพาะเมื่อทีมกำหนดไว้ใน brief หากต้องการตรวจเร็วโดยไม่ถอดรหัสทั้งไฟล์ ให้ใช้ `--skip-decode-check` แต่ควรใช้เฉพาะ preview หรือรอบพัฒนา ไม่ใช่รอบส่งมอบจริง

โหมด `--cleanup` ใช้ quarantine เป็นค่าเริ่มต้น ไม่ลบถาวร สคริปต์จะปฏิเสธไฟล์ที่อยู่นอก `job_root`, symlink, directory, final output, manifest, quality report, log, source asset หรือ first/last frame การลบถาวรต้องใช้สอง flag แยกกันคือ `--permanent-delete --confirm-permanent-delete` และไม่ควรใช้ใน production pipeline

## กรณีที่ยังต้องมีมนุษย์ตรวจ

Metadata และ decode check ไม่สามารถยืนยัน lip-sync, identity preservation, ความเป็นธรรมชาติของภาษาไทย/อีสาน, ความสวยงาม, ความถูกต้องของข่าว หรือความเหมาะสมของภาพข่าวได้ จึงต้องบันทึกผล human review หรือโมดูลเฉพาะทางใน `semantic_review` และตั้ง gate ที่จำเป็นเป็น `pass` ก่อนส่งมอบ หากยังเป็น `pending` สคริปต์จะ fail และไม่ cleanup

## สิ่งที่ workflow เดิมยังขาดและควรเติม

| ช่องว่าง | สิ่งที่ควรเพิ่ม |
|---|---|
| Decode validation | ถอดรหัสทั้งไฟล์ ไม่พึ่งเพียงสถานะ API success |
| Output integrity | บันทึก SHA-256, ขนาด, MIME และ ffprobe snapshot ของ final |
| Timing | ตรวจ audio/video drift และ captions ที่อยู่นอกช่วงวิดีโอ |
| Semantic review | แยก machine gate จาก identity, lip-sync, ภาษา และ ethics review |
| Cleanup safety | ใช้ allowlist รายไฟล์, ป้องกัน path traversal, symlink และ protected folders |
| Recovery | ย้ายไป quarantine พร้อม timestamp และบันทึก action เพื่อกู้คืนได้ |
| Idempotency | รันซ้ำได้โดยไม่ทำลายไฟล์ซ้ำและรายงาน `already_absent`/`already_quarantined` |
| Delivery evidence | เก็บ preview/contact sheet, caption coverage, sync notes และ provenance ledger |
| Operations | เพิ่ม timeout, retry, disk-space check, logging และสถานะ job เมื่อรันใน production |

## Fast preview profile และ timeout

`run_video_quality_gate.py` รองรับ `--profile preview` สำหรับรอบพัฒนา โดยยังตรวจไฟล์, ffprobe, geometry/timing, audio, captions, semantic gates และ provenance ตาม manifest แต่ข้าม full decode และ output SHA-256 เพื่อให้รอบตรวจสั้นลง ผลลัพธ์ preview มีสถานะเตือนว่าไม่ใช่ delivery gate และ **ห้ามใช้เป็นเหตุผลในการ cleanup หรือย้าย source assets ไปถังขยะ**.

ตัวอย่างคำสั่งสำหรับรอบพัฒนา:

```bash
python3 scripts/run_video_quality_gate.py manifest.json \
  --profile preview \
  --report-out quality-preview.json \
  --command-timeout 120
```

Delivery ต้องใช้ค่าเริ่มต้น `--profile delivery` ซึ่งจะทำ full decode และบันทึก output SHA-256 ก่อนอนุญาต cleanup ตามเงื่อนไขเดิม หาก `ffprobe` หรือ `ffmpeg` เกิน `--command-timeout` gate จะ fail และ cleanup จะไม่ทำงาน เพื่อป้องกัน process ค้างหรือการตัดสินผลจากข้อมูลไม่ครบ.
