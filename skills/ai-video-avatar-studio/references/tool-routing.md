# Tool Routing

ใช้เอกสารนี้เมื่อผู้ใช้ต้องการค้นหาเครื่องมือหรือเมื่อ pipeline ต้องตัดสินใจระหว่าง API กับ self-hosted GitHub ควรตรวจหน้า repository/เอกสารล่าสุด ใบอนุญาต รุ่นโมเดล น้ำหนักที่ต้องดาวน์โหลด ค่าใช้บริการ และข้อกำหนดข้อมูลก่อนใช้งานจริง ห้ามถือว่าความสามารถหรือราคาในเอกสารนี้คงที่

## หลักการเลือก

ให้ถามหรืออนุมานเฉพาะตัวแปรที่เปลี่ยนเส้นทาง ได้แก่ ระดับคุณภาพ ความเป็นส่วนตัว ความเร็ว งบประมาณ ความพร้อม GPU ความยาววิดีโอ ภาษา/สำเนียง และความต้องการ API/webhook ให้เสนออย่างน้อยสองทางเลือกเมื่อผู้ใช้ยังไม่ล็อกเครื่องมือ โดยมีทางเลือกบริการเชื่อมต่อได้และทางเลือก self-hosted ที่เบากว่า

| งาน | ตัวเลือกที่ตรวจพบ | ใช้เมื่อ | ตรวจสอบก่อนใช้งาน |
|---|---|---|---|
| Thai TTS | Google Cloud TTS, Azure Speech | ต้องการ API และเสียง neural ที่ดูแลโครงสร้างพื้นฐานน้อย | ตรวจรายการ voice `th-TH`, region, quota, data policy และ SSML/phoneme |
| Thai TTS/self-hosted | ThonburianTTS | ต้องการควบคุมข้อมูลหรือปรับเสียงด้วย runtime/GPU | ตรวจ dependency, checkpoint, VRAM, license และสิทธิ์ของ voice reference |
| Avatar/API | Azure Text to Speech Avatar หรือผู้ให้บริการ Avatar ที่มี API | ต้องการ render คุณภาพสูงและ status API | ตรวจ avatar/voice availability, async job, callback, export, watermark, cost และ consent policy |
| Lip-sync | MuseTalk | มี GPU และต้องการเชื่อมต่อเป็นโมดูล self-hosted | ตรวจ CUDA/PyTorch, model weights, VRAM, input codec, fps และ license |
| Talking face จากภาพเดียว | SadTalker | ต้องการสร้างใบหน้าพูดจากภาพนิ่งและเสียง | ตรวจภาพหน้าเต็ม แสง ขนาดใบหน้า, dependencies, GPU และ artifacts |
| Portrait motion/face animation | LivePortrait | ต้องการ driving video, retargeting หรือ regional control | ตรวจ pretrained weights, FFmpeg, GPU, image/video license และขอบเขตว่าไม่ใช่ TTS โดยตรง |
| ASR/timestamps | WhisperX | ต้องการ word-level timestamps, captions หรือ diarization | ตรวจ alignment model, language support, compute type, accuracy ของคำเฉพาะ และ model terms |
| Smart editing | Auto-Editor + FFmpeg | ต้องการตัดช่วงเงียบ/ไม่มีการเคลื่อนไหวและ render แบบ deterministic | ตรวจ padding, thresholds, codec, audio tracks และการไม่ตัดพยางค์ |

## GitHub/self-hosted route

ก่อนติดตั้งให้สร้าง environment แยก ตรวจ Python/CUDA/PyTorch/FFmpeg และทดสอบด้วยไฟล์สั้นหนึ่งชุด ดาวน์โหลด weights จากแหล่งทางการหรือ release ที่ตรวจสอบได้เท่านั้น เก็บ version/commit/hash ของ repository และ model ใน `manifest.json` อย่ารันสคริปต์ติดตั้งจาก repository ที่ไม่น่าเชื่อถือโดยไม่อ่านก่อน และอย่าเปิด endpoint สู่สาธารณะโดยไม่มี authentication

ให้ใช้ GitHub tools เป็นโมดูลเฉพาะ ไม่ควรบังคับให้โมเดลหนึ่งทำทุกอย่าง:

```text
TTS -> audio.wav
ASR/alignment -> captions.json / subtitles.ass
Avatar or portrait animation -> talking.mp4
FFmpeg/Auto-Editor -> final.mp4
quality gate -> delivery + cleanup decision
```

## API/connected route

ให้แยกขั้นตอน `submit`, `poll/status`, `download`, `verify` และ `record` เพื่อให้ retry ได้โดยไม่สร้างงานซ้ำ ใช้ idempotency key ที่ผูกกับ `job_id` เมื่อบริการรองรับ ตรวจ webhook signature หากมี callback และไม่ส่งภาพ/เสียงส่วนตัวไปยังบริการโดยไม่แจ้งผู้ใช้หรือไม่มีสิทธิ์ที่เหมาะสม

ก่อนเริ่ม render ให้ทำ preview สั้น 5–10 วินาทีเพื่อเทียบเสียง ภาพ ลิปซิงก์ และสำเนียง เมื่อ preview ไม่ผ่านให้เปลี่ยน voice/model/ภาพก่อนส่งงานเต็ม ห้ามลบต้นฉบับจาก Google Drive ในขั้น submit หรือขณะ status ยังไม่สำเร็จ

## แหล่งข้อมูลสำหรับตรวจสอบ

- [MuseTalk](https://github.com/TMElyralab/MuseTalk): lip-sync self-hosted
- [ThonburianTTS](https://github.com/biodatlab/thonburian-tts): Thai TTS self-hosted
- [SadTalker](https://github.com/OpenTalker/SadTalker): talking face จากภาพนิ่ง
- [LivePortrait](https://github.com/KlingAIResearch/LivePortrait): portrait animation
- [HeyGen developer documentation](https://developers.heygen.com/): ตัวอย่างความสามารถ API ระดับฟังก์ชันที่ควรจำลองได้ ไม่ใช่โค้ดให้คัดลอก
- [Azure Text to Speech Avatar](https://learn.microsoft.com/en-us/azure/ai-services/speech-service/text-to-speech-avatar/what-is-text-to-speech-avatar): Avatar API
- [Google Cloud voice list](https://docs.cloud.google.com/text-to-speech/docs/list-voices-and-types): ตรวจรายการเสียงล่าสุด
- [Azure language support](https://learn.microsoft.com/en-us/azure/ai-services/speech-service/language-support): ตรวจ locale/voice ล่าสุด
- [WhisperX](https://github.com/m-bain/whisperX): ASR และ word-level timestamps
- [Auto-Editor](https://github.com/WyattBlue/auto-editor): smart cut จากเสียง/การเคลื่อนไหว
- [FFmpeg Python bindings](https://github.com/kkroening/ffmpeg-python): สร้าง filtergraph แบบโปรแกรมได้

## กฎการรายงานข้อจำกัด

รายงานให้ชัดว่าเครื่องมือใดเป็น **ข้อเสนอเบื้องต้น** และข้อใดได้รับการทดสอบจริง ห้ามรับรองว่าเสียงเป็นสำเนียงอีสานโดยดูจาก `th-TH` เพียงอย่างเดียว ห้ามรับรองความสมจริงโดยไม่ดู preview และห้ามรับรองความพร้อมผลิตโดยไม่ตรวจ license, model access และ export ที่เปิดได้จริง
