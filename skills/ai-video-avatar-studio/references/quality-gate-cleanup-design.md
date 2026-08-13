# Quality Gate และ Local Cleanup Design

เอกสารนี้กำหนดสัญญาสำหรับตรวจ final video ก่อนส่งมอบและทำความสะอาดไฟล์ชั่วคราวในเครื่อง โดยยึดหลักว่า **quality gate ต้องผ่านก่อน cleanup** และ cleanup ต้องทำเฉพาะไฟล์ที่อยู่ใน allowlist ของ job เดียวกัน

## ผลลัพธ์ของ gate

| ผลลัพธ์ | ความหมาย | Cleanup |
|---|---|---|
| `pass` | ตรวจเชิงเครื่องและ metadata ผ่าน และ semantic gates ที่กำหนดครบ | อนุญาตเมื่อ manifest ให้สิทธิ์ |
| `pass_with_warnings` | ผ่านเกณฑ์บังคับ แต่มีคำเตือนที่ไม่ทำให้ส่งมอบไม่ได้ | อนุญาตเฉพาะเมื่อ `allow_warnings` เป็นจริง |
| `fail` | ตรวจไม่ผ่าน หรือข้อมูลสำคัญขาด/ขัดแย้ง | ห้าม cleanup |

## ตรวจเชิงเครื่อง

สคริปต์ต้องตรวจว่าไฟล์ final มีอยู่จริง มีขนาดมากกว่าศูนย์ อ่านด้วย `ffprobe` ได้ และมี video stream อย่างน้อยหนึ่ง stream โดยอ่าน codec, width, height, pixel format, frame rate, duration และจำนวนเฟรมเท่าที่ provider รายงานได้ หากเปิด `--decode-check` ให้ `ffmpeg` ถอดรหัสทั้งไฟล์ไปยัง null sink และหยุดเมื่อพบ decode error

หาก manifest ระบุ expected profile ให้ตรวจ geometry, aspect ratio, fps และ duration ด้วย tolerance ที่กำหนดเอง ไม่ hard-code ค่าของงานทุกประเภท ในกรณีที่ต้องมีเสียง ต้องมี audio streamและตรวจ sample rate, channels, duration และความต่างระหว่าง duration ของเสียงกับภาพ

## ตรวจ captions และ timing

หาก manifest ชี้ไปยัง captions JSON หรือ SRT ให้ตรวจช่วงเวลาไม่ติดลบ ไม่เกิน duration ของวิดีโอ และไม่เกิดช่วงที่ผิดรูปแบบ หากไม่มี captions แต่ brief ระบุว่าต้องมี ให้ fail หากคำบรรยายไม่อยู่ใน job นี้ ให้รายงาน warning แทนเมื่อไม่บังคับ

## Semantic gates ที่ต้องระบุใน manifest

การตรวจ identity preservation, lip-sync, คุณภาพภาษาไทย/อีสาน, ความสวยงามของภาพ, ความถูกต้องของข่าว และความเหมาะสมของเนื้อหาไม่ควรอนุมานจาก metadata เพียงอย่างเดียว ให้ manifest มีสถานะจาก human review หรือโมดูลตรวจเฉพาะทาง เช่น `identity_status`, `lip_sync_status`, `language_review_status`, `news_ethics_status` และ `provenance_status` หาก gate ถูกบังคับแต่ยังเป็น `pending` ให้ fail ไม่ใช่เดาเป็น pass

## Cleanup allowlist

Manifest ต้องมี `cleanup.local_candidate_paths` เป็นรายการไฟล์ชั่วคราวรายไฟล์ และระบุ `job_root` เดียวกันทุกไฟล์ สคริปต์ต้อง resolve path จริงและปฏิเสธ path ที่อยู่นอก job root, เป็น symlink, เป็น directory, เป็น final output, เป็น manifest/report/log, หรืออยู่ใน `sources/`, `final/`, `deliverables/` และโฟลเดอร์ที่ป้องกันโดยชื่อหรือ role

โหมดเริ่มต้นคือ `dry-run` ไม่แก้ไฟล์ เมื่อใช้ `--cleanup` ให้ย้ายไฟล์ไป `.cleanup-trash/<timestamp>/` เพื่อกู้คืนได้ หากต้องลบถาวรต้องใช้ `--permanent-delete --confirm-permanent-delete` แยกต่างหาก และไม่ควรใช้ใน production pipeline

## Required audit outputs

ให้เขียน `quality-report.json` ที่มี timestamp, command version, ffprobe snapshot, check results, warnings/errors, final SHA-256, cleanup preconditions และรายการ action ของ cleanup การรันซ้ำต้อง idempotent: ไฟล์ที่ย้ายไป quarantine แล้วต้องบันทึก `already_quarantined` และไม่ทำลายไฟล์ซ้ำ

## สิ่งที่ workflow เดิมยังขาด

ส่วนที่ต้องเติมให้ครบคือการตรวจ decode จริงของวิดีโอ ไม่พึ่งเฉพาะ API success, การตรวจ audio-video duration drift, การตรวจ caption ranges, การเก็บ final output hash, การแยก machine gates ออกจาก human/semantic review, การบังคับ cleanup allowlist แบบ path-safe, quarantine/recovery log, และการระบุว่าคำเตือนใดอนุญาตให้ส่งมอบได้ สิ่งเหล่านี้ควรอยู่ใน manifest เดียวกับ job status เพื่อให้ retry และ audit ได้
