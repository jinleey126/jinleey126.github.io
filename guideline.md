# Technical Blog Writing Guideline

이 문서는 Chirpy 테마를 사용하는 Youjin's AI Engineering Notes의 글 작성 기준입니다.

## 1. 글 저장 위치

모든 게시물은 `_posts/`에 저장합니다.

```text
_posts/
└── YYYY-MM-DD-descriptive-slug.md
```

파일명에는 영문 소문자, 숫자와 하이픈만 사용합니다.

## 2. 콘텐츠 분류

Chirpy는 디렉터리가 아니라 Front Matter의 `categories`와 `tags`로 글을 분류합니다.

| 상위 카테고리 | 사용 기준 | 하위 카테고리 예시 |
|---|---|---|
| Paper Reviews | 논문의 핵심 방법, 결과, 한계 분석 | LLM, RAG, Agents, Multimodal |
| Engineering Notes | 개발 중 발견한 문제 해결 방법과 팁 | Python, Backend, Data, DevOps |
| Hands-on Labs | 직접 구현하고 실습한 과정과 결과 | LLM Training, RAG, AI Agents, Model Serving |

첫 번째 category는 상위 분류, 두 번째 category는 세부 주제로 사용합니다.

## 3. Front Matter

```yaml
---
title: "검색 가능한 구체적인 제목"
description: "글이 다루는 문제와 결론을 요약한 문장"
date: 2026-07-30 09:00:00 +0900
categories:
  - Engineering Notes
  - Python
tags:
  - Python
  - Packaging
toc: true
---
```

- `title`: 문제, 기술과 분석 범위를 구체적으로 작성합니다.
- `description`: 검색 결과에서 글의 범위를 이해할 수 있는 1~2문장입니다.
- `date`: `YYYY-MM-DD HH:MM:SS +0900` 형식을 사용합니다.
- `categories`: 상위 분류와 세부 주제 순서로 최대 두 개를 권장합니다.
- `tags`: 일관된 표기로 3~5개를 사용합니다.
- `toc`: 긴 글은 `true`, 짧은 글은 `false`로 설정합니다.
- `math: true`: 수식이 있는 글에만 추가합니다.
- `mermaid: true`: Mermaid 다이어그램이 있는 글에만 추가합니다.
- `pin: true`: 홈 상단에 고정할 대표 글에만 추가합니다.

작성자는 `_config.yml`의 전역 값을 사용하므로 개별 글에 `author`를 넣지 않습니다.

## 4. 권장 글 구성

### Paper Reviews

```markdown
## 3줄 요약
## 논문이 해결하는 문제
## 핵심 아이디어
## 모델 구조 또는 알고리즘
## 실험 결과
## 장점
## 한계와 의문점
## 실무 적용 가능성
## 원문 정보
```

논문의 주장과 개인적인 해석을 구분하고, 수치에는 실험 조건을 함께 기록합니다.

### Engineering Notes

```markdown
## 상황
## 문제
## 원인
## 검토한 대안
## 적용한 해결 방법
## 핵심 코드
## 검증 결과
## 주의사항
```

독자가 재현할 수 있는 최소 코드와 환경 조건을 제공합니다.

### Hands-on Labs

```markdown
## 목표
## 환경
## 구현
## 실험 결과
## 실패와 개선
## 회고
```

연재 글은 공통 태그와 제목 순번을 사용하고 이전·다음 글을 연결합니다.

## 5. 이미지

```text
assets/img/posts/<post-slug>/
```

```markdown
![이미지 설명](/assets/img/posts/example/architecture.webp)
```

- 의미 있는 영문 파일명을 사용합니다.
- 모든 이미지에 대체 텍스트를 작성합니다.
- 외부 그림은 출처와 라이선스를 표시합니다.
- 개인정보, 내부 주소와 비밀 값이 포함된 화면은 사용하지 않습니다.

## 6. 공개 전 체크리스트

- [ ] 제목과 description만으로 글의 범위를 이해할 수 있다.
- [ ] 주장과 수치에 근거 또는 측정 조건이 있다.
- [ ] 직접 실험한 내용과 인용한 내용을 구분했다.
- [ ] 링크와 이미지 경로가 존재한다.
- [ ] Front Matter와 날짜 형식이 올바르다.
- [ ] 개인정보, 고객 정보, API 키와 NDA 자료가 없다.
- [ ] `TODO`나 placeholder가 남아 있지 않다.
- [ ] 로컬 빌드에서 오류가 없다.

## 7. 로컬 확인

```bash
bundle install
bundle exec jekyll serve
```

홈, 카테고리, 태그, 목차, 코드 블록, 다크 모드와 모바일 레이아웃을 확인합니다.
