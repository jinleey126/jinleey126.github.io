---
name: jekyll-blogger
description: Create and maintain posts for this AI engineering Jekyll blog using its collection, metadata, style, citation, and safety rules.
---

# Jekyll Blogger

새 글을 작성하기 전에 저장소 루트의 `guideline.md`를 읽고 따릅니다.

## Collection routing

- 직접 수행한 실험 → `_pages/research/`
- 논문 분석 → `_pages/papers/`
- 구현·운영·문제 해결 → `_pages/engineering/`
- 단계별 학습 연재 → `_pages/series/<series-slug>/`
- 공지 또는 일반 글 → `_posts/`

## Required checks

- Front Matter와 표준 태그 사용
- 주장·수치·출처 검증
- 이미지 출처와 라이선스 확인
- 개인정보, 내부 주소, 비밀 값과 NDA 자료 제거
- placeholder와 깨진 링크 제거
- 로컬 Jekyll 렌더링 확인
