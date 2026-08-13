# Render Pipeline and Quality Gate

ใช้เอกสารนี้เมื่อสร้างหรือแก้ไข manifest, scene plan, subtitles, audio mix, preview หรือ final export ให้ถือ `manifest.json` เป็นแหล่งความจริงเดียวของ job และเขียนสถานะทุกครั้งที่ผ่านจุดสำคัญ เพื่อให้ retry ได้โดยไม่สร้างงานซ้ำหรือลบไฟล์ผิดชุด

## Job manifest ขั้นต่ำ

```json
{
  "job_id": "av-2026-001",
  "status": "planned",
  "language": "th-TH",
  "accent": "isaan",
  "aspect_ratio": "9:16",
  "target_duration_sec": 30,
  "inputs": [
    {
      "asset_id": "img-001",
      "file_id": "google-drive-file-id",
      "sha256": "...",
      "role": "avatar_source",
      "source_url": "https://...",
      "license": "...",
      "consent_record": "consent-001"
    }
  ],
  "scenes": [
    {
      "scene_id": "s01",
      "duration_sec": 6,
      "visual_prompt": "...",
      "avatar_asset_id": "img-001",
      "audio_asset_id": "aud-001",
      "caption_range": [0.0, 6.0],
      "transition": "scene_cut"
    }
  ],
  "outputs": [],
  "cleanup": {
    "candidate_file_ids": [],
    "trash_allowed": false,
    "trashed_file_ids": []
  }
}
```

ให้เพิ่ม `tool_versions`, `model_ids`, `runtime`, `created_at`, `updated_at`, `error`, และ `quality_gate` ตามจริง ห้ามใส่ `trash_allowed: true` ก่อน final export และ quality gate ผ่านทั้งหมด

## Scene และเสียง

กำหนดหนึ่งฉากต่อหนึ่งการกระทำหลัก ใช้คลิปประมาณ 3–10 วินาทีเป็นค่าเริ่มต้นเมื่อใช้ image-to-video และเขียน transition ให้ระบุลักษณะตัวละคร การเคลื่อนที่ การเปลี่ยนสถานะ และสิ่งที่ต้องมีอยู่ตลอดฉาก สำหรับ narration ให้สร้างไฟล์เสียงแยกตามช่วงที่ sync กับฉาก และเก็บ start/end time ที่ตรวจสอบได้

เมื่อมิกซ์เสียง ให้เก็บเสียงพูด เสียงจากวิดีโอ BGM และ SFX เป็นคนละ track จนถึงขั้น final mix ลด BGM/SFX เมื่อมีคำพูด หลีกเลี่ยง clipping และตรวจช่วงต้น/ท้ายของแต่ละ track อย่าแทนที่เสียงต้นฉบับโดยไม่บันทึกเหตุผลใน manifest

## Captions และ timing

สร้าง `captions.json` จาก ASR/alignment แล้วแปลงเป็น SRT หรือ ASS เมื่อจำเป็น ตรวจชื่อบุคคล คำอีสาน ตัวเลข และเครื่องหมายวรรคตอนด้วยมนุษย์หรือกฎตรวจคำศัพท์ก่อน burn-in ให้ตรวจว่า caption ทุกบรรทัดอยู่ในช่วงวิดีโอและไม่ซ้อนกันเกินที่อ่านได้

WhisperX ให้ word-level timestamps ได้ แต่ timestamps และ alignment ยังต้องตรวจตัวอย่างจริง โดยเฉพาะคำภาษาไทย คำทับศัพท์ และเสียงที่มีดนตรีพื้นหลัง หาก timing ผิดให้แก้ audio segmentation หรือ alignment ก่อนแก้ด้วยการเร่งวิดีโอ

## Quality gate

ให้กำหนดผลเป็น `pass`, `pass_with_warnings` หรือ `fail` และแนบหลักฐาน เช่น `ffprobe.json`, thumbnail/contact sheet, preview audio, caption coverage และ sync notes

| Gate | วิธีตรวจ | เกณฑ์ขั้นต่ำ |
|---|---|---|
| File integrity | เปิดไฟล์และอ่าน metadata ด้วย ffprobe/player | เปิดได้ ไม่มี frame เสียหรือเสียงหาย |
| Geometry | ตรวจ width/height/orientation | ตรงกับ 16:9 หรือ 9:16 ตาม brief |
| Timing | เปรียบเทียบ duration ของวิดีโอ เสียง และ captions | ไม่ drift อย่างเห็นได้ชัด; ทุก caption อยู่ในช่วงวิดีโอ |
| Lip-sync | ดู preview ช่วงพยัญชนะริมฝีปากและสระยาว | ปากไม่นำ/ตามเสียงอย่างชัดเจน ไม่มี mouth artifacts รุนแรง |
| Face consistency | ดูตา ฟัน ผิว ผม มือ และฉากหลัง | ไม่มี identity drift หรือการกระพริบผิดธรรมชาติที่ทำลายงาน |
| Language | ให้เจ้าของภาษาอ่าน/ฟังตัวอย่าง | คำสำคัญและสำเนียงตรง brief |
| Audio | ตรวจ clipping, noise, speech intelligibility, BGM balance | เสียงพูดฟังชัด ไม่ถูกดนตรีกลบ |
| Captions | ตรวจตัวอย่างต้น กลาง ท้าย | ไม่มีคำผิดสำคัญ การล้นจอ หรือ timing ที่ทำให้อ่านไม่ทัน |
| Provenance | ตรวจ source/license/consent records | asset ทุกชิ้นมีบันทึกที่จำเป็น |
| Cleanup safety | ตรวจ output path, hash, status และ file IDs | ลบ/ย้ายได้เฉพาะ candidate ที่ผูกกับ job และ final ผ่าน |

## Retry และสถานะ

ใช้สถานะลำดับเดียว เช่น `planned → assets_ready → audio_ready → avatar_ready → edited → exported → quality_passed → delivered → cleanup_done` หากขั้นใดล้มเหลว ให้ตั้ง `failed` พร้อม error และหยุด cleanup ใช้ `job_id` และ hash เพื่อ reuse ผลลัพธ์ที่สำเร็จแล้ว ห้ามสร้างงานใหม่ซ้ำเมื่อมี output ที่ตรวจสอบได้
