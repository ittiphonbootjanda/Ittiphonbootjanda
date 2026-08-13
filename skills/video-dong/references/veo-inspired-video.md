# Veo-inspired Video Generation Workflow

เอกสารนี้กำหนดเวิร์กโฟลว์เชิงฟังก์ชันสำหรับการสร้างวิดีโอจากข้อความ ภาพ เสียง หรือวิดีโออ้างอิง โดยได้รับแรงบันดาลใจจากความสามารถที่เปิดเผยต่อสาธารณะของ Veo แต่ไม่คัดลอกโมเดล weights ซอร์สโค้ด อัลกอริทึมภายใน หรือส่วนติดต่อกรรมสิทธิ์ของ Google [1] [2] [3]

## ความสามารถที่เวิร์กโฟลว์ควรรองรับ

| ความสามารถ | หลักการทำงานในทักษ์ |
|---|---|
| Text-to-video | แปลง brief เป็น scene prompt ที่มี subject, environment, action, camera, lighting, style และ duration |
| Image-to-video | ใช้ภาพอ้างอิงที่ผู้ใช้มีสิทธิ์ พร้อมกำหนด motion brief โดยไม่เปลี่ยนบุคคลเดิม |
| Multi-input direction | รวม text, image, audio และ video reference ใน manifest เดียว พร้อมระบุบทบาทของแต่ละ input |
| Native/paired audio | กำหนด dialogue, ambience, sound effect และ music เป็น audio brief แยก track เพื่อควบคุมและตรวจได้ |
| Shot control | ระบุ shot size, angle, lens feel, camera motion, subject motion และ transition อย่างเป็นลำดับ |
| Scene extension | ต่อฉากจาก last frame หรือ continuity anchor ของฉากก่อน โดยตรวจเสื้อผ้า แสง ฉาก และอัตลักษณ์ |
| Frame-specific direction | ระบุ first-frame/last-frame หรือ keyframe constraints เมื่อ provider รองรับ |
| Conversational refinement | ให้แก้เฉพาะองค์ประกอบ เช่น เปลี่ยนมุมกล้อง เพิ่ม/ลดวัตถุ ปรับแสง หรือแก้เสียง โดยรักษา locked attributes |
| Short-shot assembly | สร้างคลิปสั้นที่ตรวจได้ แล้วเรียงเป็น timeline แทนการสร้างเรื่องยาวในครั้งเดียว |

## Prompt compiler

เมื่อรับคำสั่ง ให้แปลงข้อความเป็น prompt ที่มีโครงสร้างต่อไปนี้:

```yaml
scene_id: scene-001
purpose: "บทบาทของฉากในเรื่อง"
subject:
  identity_policy: preserve_exact_person | synthetic_character | non_person
  description: "ลักษณะที่ต้องคงไว้"
  action: "การกระทำที่ตรวจสอบได้ในช่วงเวลานี้"
environment:
  location: "สถานที่"
  time: "ช่วงเวลา"
  weather: "สภาพอากาศ"
  continuity_anchors: ["เสื้อผ้า", "พร็อพ", "ทิศทางแสง"]
camera:
  shot: medium
  angle: eye_level
  lens_feel: natural_documentary
  movement: slow_push_in
  framing: "วาง subject ตาม safe zone"
visual_style:
  medium: live_action | documentary | animation | stylized
  lighting: "คำอธิบายแสง"
  color: "โทนสี"
action_beats:
  - time: 0-2s
    event: "เริ่มการกระทำ"
  - time: 2-6s
    event: "เหตุการณ์หลัก"
  - time: 6-8s
    event: "จบช็อตและ hold last frame"
audio:
  dialogue: "บทพูดที่แน่นอน หรือ none"
  ambience: ["เสียงสถานที่ที่มีเหตุผล"]
  sfx: ["เสียงที่เกิดขึ้นจริงหรือระบุเป็นการออกแบบ"]
  music: "none หรือ mood/tempo"
negative_constraints: ["ห้ามเปลี่ยนใบหน้า", "ห้ามเพิ่มบุคคลที่ไม่ได้สั่ง"]
```

ไม่ควรใส่การกระทำหลายชุดที่ขัดแย้งกันในช็อตเดียว หากต้องการเหตุการณ์ต่อเนื่องให้แตกเป็นหลาย `scene_id` และส่ง last-frame/continuity state ไปฉากถัดไป

## Prompt quality rules

ให้ระบุ **shot framing and motion, style, lighting, character, location, action และ dialogue** ตามที่แหล่งข้อมูลทางการของ Google แนะนำ [2] คำอธิบายตัวละครต้องไม่สร้าง identity drift หาก `identity_policy = preserve_exact_person`; ให้ใช้ reference image เป็นหลักและกำหนดว่าใบหน้า เสื้อผ้า และลักษณะเฉพาะเป็น `locked_attributes`

การกำกับการเคลื่อนไหวควรใช้คำกริยาที่สังเกตได้ เช่น “กล้องค่อย ๆ push in 20% ใน 4 วินาที” มากกว่าคำกำกวมอย่าง “ทำให้ดูดี” สำหรับฉากซับซ้อนให้เขียนเป็น time-coded beats หรือ play-by-play และกำหนดสิ่งที่ต้องหยุด/ค้างในเฟรมสุดท้าย

สำหรับฉากพูด ให้แยกบทพูดที่ต้องตรงคำออกจากคำอธิบายอารมณ์ และกำหนดผู้พูด ตำแหน่งในเฟรม น้ำเสียง และช่วงเวลาที่พูด หากใช้ภาษาไทยหรืออีสาน ให้สร้างเสียงด้วยโมดูลเสียงที่ผ่านการทดสอบแล้ว และให้ lip-sync ใช้ audio master เดียวกับที่ส่งออก

## Continuity ledger

ก่อนสร้างฉากถัดไป ให้บันทึกและตรวจ `continuity_ledger.json` อย่างน้อย:

| ฟิลด์ | ตัวอย่าง |
|---|---|
| subject lock | `person_ref_01`, identity policy, face reference hash |
| wardrobe | สี/รูปแบบเสื้อผ้าและเครื่องประดับ |
| props | วัตถุในมือและตำแหน่ง |
| setting | สถานที่ เวลา ทิศทางแสง สภาพอากาศ |
| camera state | shot, angle, direction, focal feel |
| action state | ตำแหน่งเริ่มต้นและจุดจบของการกระทำ |
| audio state | dialogue take, ambience bed, music cue |
| last frame | path/hash ของเฟรมสุดท้ายที่อนุมัติ |

ถ้า provider รองรับ video extension หรือ last-frame control ให้ใช้ anchor ที่อนุมัติแล้ว หากไม่รองรับ ให้ใช้ภาพเฟรมสุดท้ายเป็น image reference และลดความซับซ้อนของการเปลี่ยนฉากแทนการสุ่มสร้างใหม่

## Audio design

กำหนด audio เป็นสามชั้น ได้แก่ `dialogue`, `diegetic_audio` และ `non_diegetic_audio` แล้วผสมใน post-production เมื่อจำเป็น วิธีนี้ช่วยให้แก้บทพูดโดยไม่ต้องสร้างภาพใหม่ และป้องกันการใช้เสียงประกอบที่ทำให้เหตุการณ์จริงถูกบิดเบือน

เมื่อภาพมีการกระทำที่ก่อให้เกิดเสียง ให้เขียนความสัมพันธ์ระหว่างภาพกับเสียง เช่น “ประตูปิดในวินาทีที่ 3 และมีเสียงประตูปิดหนึ่งครั้ง” หลีกเลี่ยงการสั่งเสียงที่ไม่เกิดในภาพหรือเสียงที่เพิ่มความรุนแรงเกินเหตุ โดยเฉพาะโหมดข่าว

## Generation loop

1. สร้าง brief และล็อก attributes ที่ห้ามเปลี่ยนแปลง
2. compile prompt และสร้าง preview หนึ่งหรือสองรูปแบบ
3. ตรวจ subject, composition, action, physics, text, audio และ identity
4. แก้เฉพาะฟิลด์ที่ไม่ผ่านใน `revision_request` ไม่เขียนทับ constraints ที่ผ่านแล้ว
5. สร้าง final shot และเก็บ provider/model/version/request ID ใน provenance
6. ใช้ quality gate ก่อนต่อฉากหรือส่งออก
7. ประกอบหลายช็อตด้วย render pipeline และตรวจ continuity ระหว่าง cut

ตัวอย่าง revision request:

```json
{
  "scene_id": "scene-001",
  "keep_locked": ["person_ref_01", "blue_jacket", "location", "dialogue"],
  "change_only": ["camera.movement", "lighting.contrast"],
  "request": "เปลี่ยนจาก static shot เป็น slow push-in และลด contrast ของแสงลงเล็กน้อย",
  "reason": "ตัวแบบยังเหมือนต้นฉบับ แต่ภาพมืดเกินไป"
}
```

## Quality gates

| Gate | เกณฑ์ผ่าน |
|---|---|
| Prompt adherence | subject, action, setting, camera และ duration ตรง manifest |
| Identity preservation | บุคคลเดิม ใบหน้าเดิม ไม่มี face swap หรือ drift |
| Physics/coherence | มือ วัตถุ การเคลื่อนไหว และทิศทางแสงไม่ผิดปกติอย่างมีนัยสำคัญ |
| Audio sync | dialogue ตรงปาก เสียงประกอบสัมพันธ์กับเหตุการณ์ และไม่มี clipping |
| Continuity | ฉากต่อกันโดยไม่เปลี่ยนเสื้อผ้า พร็อพ ฉาก หรือทิศทางโดยไม่มีเหตุผล |
| Editorial safety | ไม่สร้างเหตุการณ์จริงหรือหลักฐานปลอม และใช้ป้ายกำกับภาพสร้าง/ภาพจำลองเมื่อจำเป็น |
| Provenance | เก็บ input hash, model/provider, prompt, revision และ output hash |

เมื่อ gate ใดไม่ผ่าน ให้เก็บ output เป็น preview/rejected ไม่เรียกว่า final และห้ามลบ reference assets ที่จำเป็นต่อการตรวจสอบ

## ตัวอย่างโหมดข่าว

ใน `news_story_mode` ให้ใช้ Veo-inspired workflow เฉพาะกับภาพประกอบหรือ reconstruction ที่ติดป้ายชัดเจน ไม่สร้างภาพจำลองให้ดูเหมือนหลักฐานเหตุการณ์จริง และให้ใช้ source-ledger, shot-list และ ethics gate จาก [news-art-direction.md](news-art-direction.md) ร่วมด้วย

## References

[1]: https://deepmind.google/models/veo/ "Google DeepMind — Veo"
[2]: https://deepmind.google/models/veo/prompt-guide/ "Google DeepMind — How to create effective prompts with Veo 3"
[3]: https://ai.google.dev/gemini-api/docs/video "Google AI for Developers — Video generation in the Gemini API"
