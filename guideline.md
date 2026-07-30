# Technical Blog Writing Guideline

이 문서는 Satellite 테마를 사용하는 Youjin's AI Engineering Notes의 글 작성 기준입니다.

## 1. 콘텐츠 구조

Satellite는 `_pages/` 디렉터리의 폴더 구조를 블로그 탐색 구조로 사용합니다.

```text
_pages/
├── index.md
├── research/
│   ├── index.md
│   └── YYYY-MM-DD-post-slug.md
├── papers/
│   ├── index.md
│   └── YYYY-MM-DD-post-slug.md
├── engineering/
│   ├── index.md
│   └── YYYY-MM-DD-post-slug.md
└── series/
    ├── index.md
    └── series-slug/
        ├── index.md
        └── 01-post-slug.md
```

- `research`: 직접 정의한 문제, 가설, 실험 및 결과
- `papers`: 논문의 핵심 방법, 실험, 한계와 실무 적용 가능성
- `engineering`: 구현, 운영, 배포와 문제 해결 과정
- `series`: 하나의 기술을 여러 편으로 나누어 학습한 기록

새 카테고리를 만들 때는 해당 디렉터리에 `index.md`를 반드시 추가합니다.

```yaml
---
title: Engineering
---
```

## 2. 파일명

일반 글은 영문 소문자와 하이픈을 사용합니다.

```text
YYYY-MM-DD-descriptive-slug.md
```

시리즈 글은 순번을 앞에 둡니다.

```text
01-model-selection.md
02-architecture.md
```

## 3. Front Matter

```yaml
---
title: "검색 가능한 구체적인 제목"
description: "글이 다루는 문제와 결론을 요약한 문장"
date: 2026-07-30
tags:
  - Python
  - Packaging
thumbnail: "/assets/img/engineering/example/thumbnail.webp"
---
```

- `title`: 필수
- `description`: 검색 결과와 공유 미리보기에 사용할 1~2문장
- `date`: 최초 공개일, `YYYY-MM-DD` 형식
- `tags`: 일관된 표기로 3~5개
- `thumbnail`: 선택 사항이며 로컬 이미지는 `/assets/img/...` 절대 경로 사용
- `bookmark: true`: 일반 글을 사이드바에 직접 노출할 때만 사용

`layout`은 `_config.yml`에서 `page`로 지정하므로 글마다 반복하지 않습니다. 작성자도 모두 동일하므로 개별 글에 `author`를 넣지 않습니다. 외부 기고가 생길 때만 별도로 추가합니다.

## 4. 권장 글 구성

### Research

```markdown
## 요약
## 문제 정의
## 가설
## 실험 환경
## 방법론
## 결과
## 결과 해석
## 한계
## 참고 자료
```

### Paper Review

```markdown
## 3줄 요약
## 해결하려는 문제
## 핵심 아이디어
## 모델 구조 또는 알고리즘
## 실험 결과
## 장점
## 한계와 의문점
## 실무 적용 가능성
## 원문 정보
```

논문 저자는 블로그 작성자와 구분합니다.

```yaml
paper_authors:
  - First Author
  - Second Author
paper_url: "https://arxiv.org/abs/..."
```

### Engineering

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

### Series

각 글이 하나의 질문에 답하도록 작성하고, 글 상단에 전체 순서와 현재 위치를 표시합니다.

## 5. 이미지와 코드

이미지는 글의 분류와 slug에 맞춰 저장합니다.

```text
assets/img/<category>/<post-slug>/
```

```markdown
![이미지가 전달하는 내용]({{ site.baseurl }}/assets/img/engineering/example/architecture.webp)
```

- 의미 있는 영문 파일명을 사용합니다.
- 모든 이미지에 대체 텍스트를 작성합니다.
- 회사·고객의 비공개 코드, 내부 주소, 개인정보와 비밀 값은 제거합니다.
- 버전에 의존하는 예제는 라이브러리와 실행 환경을 기록합니다.
- 원문 그림과 외부 코드는 출처와 라이선스를 표시합니다.

## 6. 공개 전 체크리스트

- [ ] 제목과 설명만으로 글의 범위를 이해할 수 있다.
- [ ] 주장과 수치에 근거 또는 측정 조건이 있다.
- [ ] 직접 실험한 내용과 인용한 내용을 구분했다.
- [ ] 링크와 이미지 경로가 존재한다.
- [ ] `TODO`나 placeholder가 남아 있지 않다.
- [ ] Front Matter와 날짜 형식이 올바르다.
- [ ] 개인정보, 고객 정보, API 키와 NDA 자료가 없다.
- [ ] 로컬 빌드와 모바일 화면에서 이상이 없다.

## 7. 로컬 확인

```bash
bundle install
bundle exec jekyll serve
```

브라우저에서 사이드바, 검색, 목차, 코드 복사, 다크 모드와 모바일 레이아웃을 확인합니다.
