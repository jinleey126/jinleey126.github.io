---
name: auto-paper-reviewer
description: Fetch recent LLM papers from arXiv, generate Korean review drafts with Gemini, and save them to the papers collection for manual verification.
---

# Auto Paper Reviewer

arXiv에서 최신 LLM 논문을 수집하고 Gemini로 리뷰 초안을 생성하여 `_papers/`에 저장합니다.

## Run

```bash
GEMINI_API_KEY=... python .gemini/skills/auto-paper-reviewer/scripts/fetch_and_review.py
```

GitHub Actions에서 실행하려면 Repository Secrets에 `GEMINI_API_KEY`가 필요합니다.

자동 생성된 문서는 초안입니다. 공개 전에 `guideline.md`에 따라 다음 항목을 직접 확인합니다.

- 논문 제목, 저자, 발표일과 원문 링크
- 핵심 수식과 성능 수치
- 논문의 주장과 리뷰어 해석의 구분
- 이미지 출처와 라이선스
- placeholder와 추측성 설명

