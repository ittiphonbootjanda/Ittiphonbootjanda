## 2025-05-15 - [Accessible Character Counters & Stable Focus States]
**Learning:** For accessibility, dynamic character counters must be programmatically linked to their input via `aria-describedby` so screen reader users are aware of the constraint. For visual stability, replacing a 1px border with a 2px focus border requires reducing padding by 1px to prevent layout shift.
**Action:** Always link helper text/counters with `aria-describedby` and use padding compensation for focus borders to maintain layout integrity.
