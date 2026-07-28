## 2025-05-15 - [Maintaining Scope and Minimal Patches]
**Learning:** UX-focused agents should strictly avoid non-essential formatting or reformatting of non-frontend files (like backend logic) to keep PRs focused and under the 50-line limit. Unintended artifacts like `__pycache__` and local logs must be excluded from commits.
**Action:** Always check `git status` and `git diff` before committing to ensure only intended UX changes are included and artifacts are cleaned up. Revert any accidental reformatting in files outside the immediate scope.
