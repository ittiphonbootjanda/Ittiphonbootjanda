# Speed Optimization สำหรับวีดีโด่ง

เอกสารนี้กำหนดวิธีลดเวลาผลิตวิดีโอโดยไม่ลด **identity preservation, consent, provenance, semantic review หรือ delivery quality gate**. หลักสำคัญคือแยกงานทดลองออกจากงานส่งมอบ และลดเวลารอที่ไม่จำเป็นแทนการปิดการตรวจคุณภาพ

## ช่องทางที่ช่วยให้เร็วขึ้น

| ช่องทาง | เหมาะกับงาน | วิธีลดเวลา | ข้อควรระวัง |
|---|---|---|---|
| **Preview path** | ทดลอง prompt, framing, timing และ lower-third | ใช้ proxy/scene สั้น, preview audio และ `--profile preview` | ไม่ใช่ delivery gate และห้าม cleanup |
| **Parallel preflight + TTL cache** | รอบทดลองที่ตรวจเครื่องมือซ้ำบ่อย | ใช้ `--workers` และ cache เฉพาะผล read-only ที่ผ่าน | ก่อน mutation ต้องรัน fresh preflight |
| **DAG/bounded concurrency** | หลาย asset, หลาย scene หรือหลายภาษา | ทำ node ที่ไม่พึ่งกันพร้อมกัน จำกัดตาม VRAM, rate limit และ disk | อย่าขนานเกิน capacity จนเกิด VRAM thrashing หรือ 429 |
| **Local/self-hosted GPU** | ข้อมูลใบหน้า/เสียงที่ไม่ควรออกนอกระบบ หรือมี GPU พร้อม | โหลด model ค้างใน worker และ reuse avatar preparation | ต้องตรวจ license, CUDA/PyTorch, VRAM และ data retention |
| **ComfyUI API** | workflow สร้างภาพ/เฟรมที่ต้องการ queue และ preview | HTTP submit, WebSocket progress และ history/output retrieval; WebSocket รับภาพระหว่างทำได้ [1] | ต้อง pin workflow/model และเก็บ job/output provenance |
| **Runpod Serverless** | งาน GPU แบบ batch หรือ async ที่ไม่ต้องดูแลเครื่องเอง | queue-based `/run`, webhook, worker scaling และ model caching [2] [3] | ต้องจัดการ TTL, timeout, provider job ID, webhook retry และค่าใช้จ่าย |
| **Modal Web Functions** | inference service ที่ต้อง scale ตามโหลด | container แบบ on-demand และ `@modal.concurrent` สำหรับ concurrent inputs เมื่อเหมาะสม [4] | cold start และความเหมาะสมของ concurrency ต้องวัดจริง |
| **Hardware encode/decode** | proxy และ encode จำนวนมาก | ใช้ GPU codec เมื่อเครื่องและปลายทางรองรับ | ต้องตรวจ codec compatibility; final profile ต้องผ่าน full gate |

## รูปแบบที่แนะนำ

ให้ใช้เส้นทางสองระดับ. **Preview path** ใช้เพื่อ feedback loop ที่เร็ว โดยลดความละเอียดหรือระยะเวลาของคลิป และตรวจ structural/caption/semantic checks ที่จำเป็นต่อการแก้ไข แต่ไม่ทำ full decode และไม่บันทึก output hash ทุกครั้ง. **Delivery path** ใช้ความละเอียดจริง, full decode, output SHA-256, provenance, human/semantic review และ cleanup หลัง final artifacts เปิดอ่านได้จริงเท่านั้น.

ให้สร้าง job เป็น dependency graph. Asset fetch, license/provenance lookup, TTS ของฉากที่แยกกัน และ ASR/alignment ที่ไม่พึ่งกันสามารถทำพร้อมกันได้. Avatar preparation ควร reuse เมื่อ `source_sha256 + model_id + settings_hash + consent_id` ตรงกัน. Scene generation ควรมี bounded concurrency ตาม VRAM และ provider rate limit. Mix, final encode, quality gate และ Drive trash ต้องเป็นขั้นที่ลำดับชัดเจนและบันทึกสถานะใน manifest.

สำหรับ provider ที่ใช้เวลานาน ให้ใช้สัญญา `submit → status/webhook → download → verify → record`. Runpod ระบุว่า `/run` เหมาะกับงาน asynchronous และมี `/status`, `/stream` และ webhook สำหรับติดตามผล [2]. Webhook ต้องตรวจ signature และ provider job ID; เมื่อ webhook หายให้ fallback เป็น status query แบบ backoff. หาก timeout แล้วไม่รู้ว่าคำสั่งสำเร็จหรือไม่ ให้บันทึก `unknown_after_timeout` และค้นหาผลเดิมด้วย idempotency key ก่อนส่งซ้ำ.

## คำสั่งที่ใช้กับทักษ์

รอบทดลองสามารถลดเวลาตรวจ connector ที่เป็น read-only ได้ดังนี้:

```bash
python3 scripts/preflight_integrations.py \
  --workers 8 \
  --cache-file .cache/preflight.json \
  --cache-ttl-sec 300 \
  --report-out connection-preflight-report.json
```

ก่อนส่งมอบให้รัน Quality Gate เต็มรูปแบบตามค่าเริ่มต้น:

```bash
python3 scripts/run_video_quality_gate.py \
  manifest.json \
  --profile delivery \
  --report-out quality-report.json \
  --command-timeout 300
```

สำหรับรอบทดลองที่ไม่ทำ cleanup:

```bash
python3 scripts/run_video_quality_gate.py \
  manifest.json \
  --profile preview \
  --report-out quality-preview.json \
  --command-timeout 120
```

## การวัดผลก่อนเลือกช่องทาง

อย่าเลือก provider จากคำโฆษณาเรื่องความเร็วเพียงอย่างเดียว ให้บันทึกเวลา `preflight`, `asset_fetch`, `tts`, `asr_alignment`, `avatar_prepare`, `scene_generate`, `edit_encode`, `quality_gate` และ `drive_verify`. เปรียบเทียบ p50/p95 จากงานที่ใช้ input hash, model version, resolution และ duration เดียวกัน. ต้องวัดทั้งเวลารอคิว, cold start, processing, download และ verification เพราะช่องทางที่เร็วใน inference อาจช้ากว่าหลังรวม transfer และ quality gate.

## ข้อห้ามเพื่อแลกความเร็ว

ห้ามปิด identity gate, consent, provenance, file verification หรือ semantic review ใน delivery. ห้ามย้าย source assets ไปถังขยะก่อน final video และ quality report ผ่าน. ห้าม retry upload/move/trash/submit หลัง timeout หากยังไม่ค้นหาผลเดิม. ห้ามทำงานขนานแบบไร้ขอบเขต และห้าม fallback ไป provider ใหม่โดยไม่แจ้งผู้ใช้และตรวจนโยบายข้อมูล.

## References

[1]: https://docs.comfy.org/development/comfyui-server/api-examples "ComfyUI — API Examples"

[2]: https://docs.runpod.io/serverless/endpoints/send-requests "Runpod — Send API requests"

[3]: https://docs.runpod.io/serverless/endpoints/overview "Runpod — Serverless Endpoints Overview"

[4]: https://modal.com/docs/guide/webhooks "Modal — Web Functions"

[5]: https://github.com/TMElyralab/MuseTalk "MuseTalk — Official GitHub repository"

[6]: https://github.com/m-bain/whisperX "WhisperX — Official GitHub repository"
