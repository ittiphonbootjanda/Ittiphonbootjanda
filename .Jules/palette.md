## 2025-05-22 - Layout Stability during Focus States
**Learning:** When adding a border for focus states (e.g., replacing a 1px border with a 2px border or adding a 2px border to an element without one), the padding must be reduced by the exact width of the border increase to maintain consistent box dimensions and prevent layout "jumps".
**Action:** Always calculate the total box size (content + padding + border) and ensure it remains identical between normal and focus states by adjusting padding accordingly.
