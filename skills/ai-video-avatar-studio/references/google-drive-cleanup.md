# Google Drive Storage and Cleanup

ใช้ `gws` CLI ตามแนวทาง Google Workspace ที่ติดตั้งในสภาพแวดล้อม ห้ามลบไฟล์จริงจนกว่า final video จะถูกอัปโหลดและเปิดอ่านได้ จากนั้นให้ย้ายเฉพาะไฟล์ต้นฉบับที่ติดตามด้วย `fileId` ไปถังขยะ ไม่ลบถาวร

## โครงสร้างโฟลเดอร์

ให้สร้างหรือใช้โฟลเดอร์แยกต่อ job เช่น:

```text
AI Video Avatar Studio/
└── {job_id}/
    ├── sources/
    ├── working/
    ├── previews/
    ├── final/
    └── logs/
```

ให้เก็บ `job_id`, folder IDs, file IDs, source URL, author, license, consent record, SHA-256, MIME type, size และเวลาที่อัปโหลดไว้ใน manifest อย่าติดตามด้วยชื่อไฟล์เพียงอย่างเดียว เพราะชื่อซ้ำหรือถูกเปลี่ยนได้

## คำสั่งตัวอย่าง

ตรวจ schema และสิทธิ์ก่อนใช้คำสั่งจริงเมื่อพารามิเตอร์เปลี่ยนหรือไม่แน่ใจ:

```bash
gws schema drive.files.create --resolve-refs
gws schema drive.files.update --resolve-refs
```

อัปโหลดไฟล์โดยเก็บ response JSON เพื่อบันทึก `id`, `name`, `mimeType`, `size`, `parents`, `md5Checksum` หรือ metadata ที่มี:

```bash
gws drive files create \
  --json '{"name":"source-001.jpg","parents":["FOLDER_ID"]}' \
  --upload "/path/to/source-001.jpg" \
  --upload-content-type "image/jpeg"
```

ตรวจไฟล์หลังอัปโหลดโดยขอ fields ที่จำเป็น:

```bash
gws drive files get \
  --params '{"fileId":"FILE_ID","fields":"id,name,mimeType,size,md5Checksum,parents,trashed,webViewLink"}'
```

อัปโหลด final เข้าโฟลเดอร์ final แล้วตรวจ response และดึง metadata ก่อนอนุญาต cleanup:

```bash
gws drive files create \
  --json '{"name":"video.mp4","parents":["FINAL_FOLDER_ID"]}' \
  --upload "/path/to/video.mp4" \
  --upload-content-type "video/mp4"
```

ย้ายไฟล์ต้นฉบับไปถังขยะด้วย `trashed: true` หลังผ่านเงื่อนไขทั้งหมด:

```bash
gws drive files update \
  --params '{"fileId":"SOURCE_FILE_ID"}' \
  --json '{"trashed":true}'
```

หลังย้ายให้ตรวจ `trashed: true` และบันทึก response ลง `cleanup-log.json` ห้ามใช้คำสั่งลบถาวรในทักษะนี้

## Cleanup preconditions

อนุญาต cleanup เมื่อทุกข้อเป็นจริง:

1. `status` เป็น `quality_passed` หรือ `delivered` และไม่มี error ที่ยังไม่แก้
2. final video มี `fileId`, ขนาดมากกว่าศูนย์, MIME type ถูกต้อง และเปิดอ่าน metadata ได้
3. มีการตรวจ preview หรือ final จริง ไม่ใช่เพียง API ตอบ `success`
4. candidate file IDs อยู่ใน manifest และตรงกับ asset ที่ใช้ใน job นี้เท่านั้น
5. source URL/license/consent และ SHA-256 ถูกบันทึกแล้ว
6. ไม่ใช่ไฟล์ที่ผู้ใช้อัปโหลดมาเพื่อเก็บถาวร ไม่ใช่ไฟล์ใน job อื่น และไม่มีสถานะ locked/retained
7. ยังไม่มี `cleanup_done: true` หรือถ้ามี ให้ตรวจซ้ำแบบ idempotent ก่อนข้าม

หากข้อใดไม่ผ่าน ให้ตั้ง `trash_allowed: false`, ไม่ย้ายไฟล์ และรายงานสาเหตุให้ผู้ใช้ทราบ

## ความปลอดภัยและการกู้คืน

ให้ขอการยืนยันก่อน cleanup เมื่อผู้ใช้ไม่ได้สั่งลบไว้อย่างชัดเจน หรือเมื่อ candidate มีไฟล์หลายประเภท/อยู่ในโฟลเดอร์ที่แชร์ หากผู้ใช้สั่งอัตโนมัติไว้แล้ว ให้ย้ายไปถังขยะได้หลัง quality gate แต่ต้องบันทึก file IDs ทุกไฟล์

อย่าลบหรือย้ายโฟลเดอร์ job ทั้งหมดโดยอัตโนมัติ ให้ย้ายเฉพาะ source files ที่มี `role` เป็น `avatar_source`, `image_reference` หรือ `temporary_download` และถูกระบุเป็น candidate รายไฟล์ การย้ายไปถังขยะต้องทำซ้ำได้: ตรวจสถานะก่อน ถ้า `trashed` อยู่แล้วให้บันทึกว่า `already_trashed` ไม่เรียกซ้ำโดยไม่จำเป็น

ตัวอย่าง `cleanup-log.json`:

```json
{
  "job_id": "av-2026-001",
  "preconditions": {
    "final_uploaded": true,
    "final_verified": true,
    "quality_gate": "pass",
    "user_authorized_auto_trash": true
  },
  "files": [
    {"file_id":"...","action":"trash","status":"trashed"},
    {"file_id":"...","action":"trash","status":"already_trashed"}
  ],
  "completed_at": "2026-08-14T00:00:00Z"
}
```

หาก API ส่ง error, token หมดอายุ, สิทธิ์ไม่พอ หรือ final ตรวจไม่ได้ ให้หยุด cleanup ทันทีและเก็บต้นฉบับไว้ ผู้ใช้สามารถกู้คืนไฟล์จากถังขยะของ Google Drive ได้ตามนโยบายของบัญชี แต่ทักษะนี้ต้องไม่พยายามลบถาวรหรือกู้คืนแทนผู้ใช้โดยอัตโนมัติ
