---
name: ai-video-avatar-studio
description: End-to-end AI video avatar production from authorized images, scripts, and voice. Use for Thai or Isaan-speaking avatars, image-to-video, lip-sync, portrait animation, consented face editing, automatic captions, smart editing, tool discovery from GitHub or APIs, Google Drive asset storage, and post-export cleanup.
---

# AI Video Avatar Studio

สร้างวิดีโอ Avatar และวิดีโอจากภาพแบบครบวงจร โดยใช้หลักการระดับฟังก์ชันของแพลตฟอร์มสมัยใหม่เท่านั้น ห้ามคัดลอกซอร์สโค้ด โมเดลปิด อัลกอริทึมลับ เครื่องหมายการค้า หรือส่วนติดต่อผู้ใช้ของผู้ให้บริการใด

## ขอบเขตและกฎหยุดงาน

ใช้ทักษะนี้เมื่อผู้ใช้ต้องการสร้างวิดีโอพูด ลิปซิงก์จากภาพ สร้าง Avatar จากภาพหรือเสียง สร้างเสียงภาษาไทย/อีสาน ทำภาพเคลื่อนไหว ปรับเปลี่ยนใบหน้าแบบได้รับความยินยอม ตัดต่ออัตโนมัติ ค้นหาเครื่องมือจาก GitHub/API หรือจัดการ asset ใน Google Drive

ก่อนเริ่มงานราคาแพงหรือเริ่ม render ให้รวบรวมเป้าหมาย กลุ่มผู้ชม ความยาว อัตราส่วน สไตล์ ภาษา/สำเนียง แหล่งภาพ เสียงอ้างอิง อัตราคุณภาพ ปลายทาง และเงื่อนไขการลบไฟล์ หากข้อมูลสำคัญยังขาด ให้ถามก่อน ห้ามเดาโดยเฉพาะเรื่องสิทธิ์ ใบหน้า เสียง และการลบข้อมูล หากผู้ใช้ยืนยันให้ดำเนินการและบรีฟครบถ้วนแล้ว ให้สรุปแผนสั้น ๆ และเริ่มงานได้

ห้ามประมวลผลภาพ ใบหน้า เสียง หรือวิดีโอของบุคคลจริงเมื่อผู้ใช้ไม่มีสิทธิ์หรือความยินยอมที่เหมาะสม ห้ามสร้างเนื้อหาที่แอบอ้างเป็นบุคคลจริงเพื่อหลอกลวง ห้ามใช้ภาพที่ค้นจากเว็บโดยไม่ตรวจใบอนุญาต และห้ามเผยแพร่ข้อมูลระบุตัวตนเกินความจำเป็น เมื่อสิทธิ์ไม่ชัดเจน ให้หยุดและเสนอทางเลือก เช่น Avatar สังเคราะห์ ใบหน้าที่สร้างใหม่ หรือสื่อที่มีใบอนุญาตชัดเจน

## เวิร์กโฟลว์มาตรฐาน

1. **รับบรีฟและกำหนด job ID** ให้สร้าง `job_id`, ระบุ input/output, language, aspect ratio, duration, quality target และสถานะงาน
2. **ตรวจสิทธิ์และ provenance** ให้บันทึกแหล่งที่มา URL ผู้สร้าง ใบอนุญาต หลักฐานความยินยอม และ SHA-256 ของไฟล์ใน manifest ก่อนอัปโหลดหรือสร้างผลลัพธ์
3. **วางสคริปต์และฉาก** ให้แยกบทพูด คำบรรยาย B-roll จังหวะกล้อง อารมณ์ เสียงประกอบ และจุดเปลี่ยนฉากเป็น scene manifest ห้ามยัดหลายการกระทำที่ไม่ต่อเนื่องไว้ในคลิปเดียว
4. **เลือกเส้นทางเครื่องมือ** ให้เปรียบเทียบ API/บริการเชื่อมต่อได้กับ GitHub/self-hosted ตามคุณภาพ ความเป็นส่วนตัว GPU เวลา ใบอนุญาต และค่าใช้จ่าย อ่าน [tool-routing.md](references/tool-routing.md) เมื่อจำเป็นต้องเลือกหรือค้นหาเครื่องมือ
5. **ค้นหาและจัดเก็บ asset** ให้ค้นจากแหล่งที่อนุญาต ดาวน์โหลดเฉพาะไฟล์ที่จำเป็น บันทึก provenance แล้วอัปโหลดเข้าโฟลเดอร์ job ใน Google Drive โดยใช้แนวทางใน [google-drive-cleanup.md](references/google-drive-cleanup.md)
6. **เตรียมเสียง** ให้เลือกเสียงภาษาไทยจาก provider ที่รองรับ locale `th-TH` หรือใช้ ThonburianTTS เมื่อมี runtime/GPU เหมาะสม สำหรับภาษาอีสาน ให้ตรวจสคริปต์โดยเจ้าของภาษา กำหนดคำอ่าน/การเว้นวรรค และทำตัวอย่างสั้นก่อนสร้างทั้งงาน อ่าน [thai-isaan-voice.md](references/thai-isaan-voice.md)
7. **สร้าง Avatar และลิปซิงก์** ให้เลือกบริการ Avatar/API เมื่อผู้ใช้ต้องการคุณภาพสูงและไม่ดูแล GPU หรือเลือก MuseTalk, SadTalker, LivePortrait และโมดูลที่เหมาะสมเมื่อ self-hosted ให้ตรวจ identity drift, ปาก/ฟัน/ตา, การกะพริบ, ศีรษะ, มือ และฉากหลัง
8. **สร้าง image-to-video/B-roll** ให้ใช้ภาพอ้างอิงที่มีสิทธิ์และกำหนดการเคลื่อนไหวแบบสั้นต่อฉาก รักษาอัตราส่วน 16:9 หรือ 9:16 เป็นค่าเริ่มต้น และตรวจความต่อเนื่องของตัวละคร/วัตถุ
9. **ทำคำบรรยายและ timing** ให้ใช้ WhisperX หรือบริการที่เชื่อมต่อได้เพื่อสร้าง word-level timestamps และ SRT/ASS จากนั้นตรวจคำสำคัญ ภาษาไทย/อีสาน และการเหลื่อมของเวลา อย่าเชื่อ timestamps โดยไม่ตรวจตัวอย่างจริง
10. **ตัดต่อและมิกซ์เสียง** ให้ตัดช่วงเงียบแบบ conservative ด้วย Auto-Editor/FFmpeg เติม captions, B-roll, text overlay, music และ sound effects ตาม manifest รักษาเสียงทุก track ด้วยการ overlay ไม่ใช่แทนที่ และควบคุมเสียงพูดให้เด่นกว่าดนตรี
11. **ผ่าน quality gate** ให้ตรวจไฟล์เปิดได้ duration อัตราส่วน frame ไม่เสีย sync ปาก/เสียง คำบรรยายครอบคลุม pronunciation ระดับเสียง watermark ใบอนุญาต และความต่อเนื่อง อ่าน [render-pipeline.md](references/render-pipeline.md)
12. **ส่งมอบและ cleanup** ให้บันทึก final video, manifest, quality report และ log ใน Google Drive ก่อนย้ายภาพต้นฉบับที่ผูกกับ job ไปถังขยะ อ่าน [google-drive-cleanup.md](references/google-drive-cleanup.md) ห้ามลบถาวร

## Veo-inspired generation mode

เมื่อผู้ใช้ต้องการสร้างวิดีโอจากข้อความ ภาพ เสียง หรือวิดีโออ้างอิง ให้ใช้ workflow ใน [veo-inspired-video.md](references/veo-inspired-video.md) ซึ่งจำลองหลักการระดับฟังก์ชันที่เปิดเผยต่อสาธารณะ เช่น prompt compiler, shot framing and motion, image-based direction, native/paired audio, scene extension, last-frame continuity, conversational refinement และการประกอบคลิปสั้นเป็นเรื่องเดียว ห้ามเรียกสิ่งนี้ว่าเป็นการโคลน Veo และห้ามคัดลอกโมเดล ซอร์สโค้ด อัลกอริทึมปิด หรือทรัพย์สินทางปัญญาของผู้ให้บริการ

ให้สร้าง `scene-plan.json`, `prompt-pack.json`, `continuity-ledger.json` และ `audio-plan.json` ก่อนเริ่ม render โดยล็อก `preserve_exact_person`, เสื้อผ้า พร็อพ ฉาก บทพูด และคุณสมบัติอื่นที่ผู้ใช้กำหนดว่าห้ามเปลี่ยนแปลง สร้างทีละช็อตหรือทีละฉาก ใช้ time-coded action beats กับคำสั่งกล้องที่วัดได้ และทำ revision เฉพาะองค์ประกอบที่ไม่ผ่าน quality gate

หากเครื่องมือรองรับ ให้ใช้ภาพอ้างอิง เฟรมแรก เฟรมสุดท้าย หรือ video extension เพื่อรักษาความต่อเนื่องระหว่างฉาก หากไม่รองรับ ให้ใช้เฟรมสุดท้ายที่ผ่านการอนุมัติเป็น reference ใหม่และลดความซับซ้อนของการเปลี่ยนฉาก ห้ามสร้างบุคคลเดิมขึ้นใหม่โดยไม่มี reference เพราะเสี่ยงทำให้ใบหน้าและอัตลักษณ์เปลี่ยน ใช้ `scripts/sync_frame_controls_to_drive.py` เพื่ออัปโหลดหรือผูกเฟรมกับ Google Drive และสร้าง manifest ที่ตรวจสอบได้

กำหนดเสียงเป็น `dialogue`, `diegetic_audio` และ `non_diegetic_audio` แยกกัน ตรวจว่าเสียงพูดตรงกับปากและเหตุการณ์ที่เห็น และในโหมดข่าวต้องไม่เพิ่มเสียงหรือภาพที่ทำให้เหตุการณ์จริงถูกบิดเบือน

## การเลือกเส้นทางโดยเร็ว

| ความต้องการ | เส้นทางเริ่มต้น | เงื่อนไขเปลี่ยนเส้นทาง |
|---|---|---|
| คุณภาพสูง ไม่ต้องติดตั้ง GPU | API/บริการ Avatar และ TTS ที่มี endpoint | ตรวจราคา region เสียงภาษาไทย/นโยบายข้อมูล และ webhook/status API ก่อน |
| ควบคุมข้อมูลและมี GPU | GitHub/self-hosted เช่น MuseTalk, SadTalker, LivePortrait, ThonburianTTS | ตรวจ license, model weights, CUDA/PyTorch, VRAM และเวลา render |
| ต้องการภาพเคลื่อนไหวจาก driving video | LivePortrait หรือเครื่องมือ portrait animation | ใช้ lip-sync แยกต่างหากหากโมดูลไม่รับเสียงโดยตรง |
| ต้องการพูดจากภาพเดียว | SadTalker หรือ talking-avatar API | ทดสอบภาพหน้าเต็ม แสง และขนาดใบหน้าก่อน render ทั้งชุด |
| ต้องการลิปซิงก์เสียงแม่น | MuseTalk หรือ API lip-sync | ตรวจ alignment, fps, codec และเสียงต้นฉบับ |
| ต้องการตัดต่อเร็ว | Auto-Editor + FFmpeg + WhisperX | ตั้ง padding และตรวจไม่ให้ตัดพยางค์/ลมหายใจ |

## ข้อกำหนดคุณภาพเริ่มต้น

ให้ตั้งค่าเสียงเป็น PCM/WAV ระหว่างทำงาน และส่งออกวิดีโอด้วย codec ที่ปลายทางรองรับ ตรวจ `fps`, `duration`, `width`, `height`, audio sample rate และ loudness ให้สอดคล้องกันตลอด pipeline แบ่งงานเป็นคลิปสั้นหรือฉากที่ตรวจได้ง่าย และเก็บ intermediate ที่จำเป็นจนกว่า final จะผ่าน quality gate

สำหรับวิดีโอที่ต่อเนื่อง ให้ใช้เฟรมสุดท้ายของคลิปก่อนหน้าเป็นจุดเริ่มของคลิปถัดไปเมื่อเครื่องมือรองรับ หลีกเลี่ยงการสร้างภาพใหม่โดยไม่ใช้ reference เพราะทำให้ใบหน้า เสื้อผ้า และฉากเปลี่ยนโดยไม่ตั้งใจ สร้างเสียง TTS แยกตามช่วง narration ที่พอดีกับฉาก ไม่สร้างเสียงยาวก้อนเดียวจนควบคุม timing ไม่ได้

## สัญญาไฟล์และผลลัพธ์

ให้สร้างไฟล์หรือรายการต่อไปนี้ทุก job ตามความเหมาะสม:

```text
job_id/
├── manifest.json
├── source-provenance.json
├── script-scenes.json
├── audio/
├── captions/
├── previews/
├── final/
│   └── video.mp4
├── quality-report.json
└── cleanup-log.json
```

ให้รายงานผลด้วยลิงก์หรือ path ของวิดีโอสุดท้าย สรุปเครื่องมือและรุ่นที่ใช้ ภาษา/เสียง อัตราส่วนและความยาว ผล quality gate คำเตือน แหล่งที่มา และรายการไฟล์ที่ย้ายไปถังขยะ หากงานล้มเหลวให้รายงานจุดที่ล้มเหลวและเก็บภาพต้นฉบับไว้

## การอ้างอิงที่ต้องอ่านเมื่อจำเป็น

- **การเลือกเครื่องมือและการเชื่อมต่อ:** [tool-routing.md](references/tool-routing.md)
- **ภาษาไทยและภาษาอีสาน:** [thai-isaan-voice.md](references/thai-isaan-voice.md)
- **manifest, captions, audio mix และ quality gate:** [render-pipeline.md](references/render-pipeline.md)
- **Veo-inspired prompt, shot control, continuity และ audio workflow:** [veo-inspired-video.md](references/veo-inspired-video.md)
- **First/last-frame control กับ Google Drive:** [frame-control-google-drive.md](references/frame-control-google-drive.md)
- **Google Drive, การติดตาม file ID และการย้ายไปถังขยะ:** [google-drive-cleanup.md](references/google-drive-cleanup.md)
- **consent, likeness, copyright และ provenance:** [safety-consent.md](references/safety-consent.md)

## ข้อห้ามที่ไม่เปลี่ยนแปลง

ห้ามข้าม consent gate ห้ามใช้คำว่า “รองรับภาษาอีสาน” โดยไม่มีการทดสอบเสียงจริง ห้ามลบไฟล์ Google Drive แบบถาวร ห้ามลบต้นฉบับก่อน final export และ quality gate สำเร็จ ห้ามอ้างว่าเป็นการโคลน HeyGen, CapCut หรือ Veo ให้เรียกว่า workflow ที่ได้รับแรงบันดาลใจจากความสามารถสาธารณะและใช้ implementation ที่ถูกต้องตามสิทธิ์
