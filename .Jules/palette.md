## 2025-05-14 - [Layout Stability during Focus]
**Learning:** Adding a border on focus can cause layout jitter if not compensated by reducing padding. For the textarea, reducing padding from 10px to 9px when adding a 2px border (replacing a 1px border) keeps the element size stable.
**Action:** Always ensure that focus state style changes (like border width) are offset by padding or margin adjustments to maintain visual stability.
