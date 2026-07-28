## 2025-06-03 - [Preventing Layout Shift on Focus]
**Learning:** Adding a border to an element on focus (e.g., for accessibility) can increase its total box size and cause layout shifts if the element doesn't already have a border of the same width.
**Action:** Always compensate for new focus borders by either using `box-shadow` (which doesn't affect layout) or by reducing the element's `padding` by the width of the added border.
