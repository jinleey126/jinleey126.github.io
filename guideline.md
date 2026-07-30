# Technical Blog Writing Guideline

이 문서는 Youjin's AI Engineering Notes에 새 글을 추가하거나 기존 글을 수정할 때 사용하는 운영 기준입니다.

## 1. 블로그 목적

이 블로그는 다음 내용을 공개 가능한 기술 지식으로 축적합니다.

- 직접 수행한 AI 연구와 실험
- 논문의 핵심 구조와 실무 적용 가능성
- Production AI 시스템의 구현 및 문제 해결 과정
- 하나의 기술을 단계적으로 탐구한 학습 연재

프로젝트 성과 소개는 `portfolio/`, 회사별 지원 자료는 `applied/`에서 관리합니다. 이 블로그에는 재사용 가능한 기술적 통찰과 검증 가능한 공개 정보만 작성합니다.

## 2. 콘텐츠 분류

새 글을 작성하기 전에 목적에 맞는 컬렉션을 선택합니다.

| 컬렉션 | 경로 | 사용 기준 |
|---|---|---|
| Research | `_research/` | 본인이 문제와 가설을 정의하고 직접 실험한 결과 |
| Paper Reviews | `_papers/` | 타인의 논문을 읽고 핵심 방법, 결과, 한계를 분석한 글 |
| Engineering | `_engineering/` | 구현, 운영, 배포, 테스트, 장애 및 성능 문제 해결 기록 |
| Learning Series | `_series/<series-name>/` | 하나의 주제를 순서대로 학습하거나 구현하는 연재 |
| Posts | `_posts/` | 위 분류에 포함되지 않는 공지와 일반 기술 글 |

분류가 애매한 경우 다음 질문으로 판단합니다.

- 내가 세운 가설과 직접 측정한 결과가 중심인가? → Research
- 특정 논문의 기여와 한계를 설명하는가? → Paper Reviews
- 재현 가능한 구현 또는 문제 해결 절차가 중심인가? → Engineering
- 여러 편이 순서대로 연결되는가? → Learning Series

## 3. 파일명 규칙

영문 소문자와 하이픈을 사용합니다.

```text
YYYY-MM-DD-descriptive-slug.md
```

예:

```text
2026-07-30-fastapi-sse-disconnection-handling.md
2026-07-30-lora-mora-memory-comparison.md
```

시리즈는 디렉터리와 순번을 함께 사용합니다.

```text
_series/qwen-image-training/
├── 01-model-selection-and-setup.md
├── 02-architecture-and-performance.md
└── 03-dataset-preprocessing.md
```

파일명에는 공백, 한글, 괄호, 중복 하이픈을 사용하지 않습니다.

## 4. Front Matter

모든 글은 다음 메타데이터로 시작합니다.

```yaml
---
title: "독자가 검색할 수 있는 구체적인 제목"
description: "글의 문제와 결론을 설명하는 1~2문장"
date: 2026-07-30
category: engineering
subcategory: llm-serving
tags:
  - FastAPI
  - vLLM
  - LLM
layout: post
mermaid: false
---
```

시리즈에는 다음 필드를 추가합니다.

```yaml
series: qwen-image-training
series_order: 3
```

필드 작성 원칙:

- `title`: 기술명만 쓰지 않고 해결한 문제나 분석 범위를 포함합니다.
- `description`: 검색 결과에서 글을 이해할 수 있도록 120~160자 이내로 작성합니다.
- `date`: 최초 공개일을 사용합니다. 단순 수정 시 변경하지 않습니다.
- `category`: 컬렉션의 목적과 일치시킵니다.
- `tags`: 사전에 정의한 표기를 사용하며 3~5개로 제한합니다.
- `mermaid`: Mermaid 다이어그램이 있을 때만 `true`로 설정합니다.

작성자는 `_config.yml`의 전역 `author` 값을 사용하므로 개별 글에서 반복하지 않습니다. 외부 기고자가 작성한 글에만 `author`를 별도로 지정합니다. 논문 저자는 작성자와 구분하여 다음처럼 기록합니다.

```yaml
paper_authors:
  - First Author
  - Second Author
paper_url: "https://arxiv.org/abs/..."
```

## 5. 태그 표준

가능하면 다음 표기를 재사용합니다.

```text
LLM
RAG
AI Agent
PEFT
LoRA
MoRA
Tokenizer
NLP
Table QA
Multimodal
PyTorch
FastAPI
vLLM
DeepSpeed
Data Engineering
Testing
Infrastructure
Paper Review
```

같은 기술을 `fastapi`, `Fast API`, `FastAPI`처럼 다르게 표기하지 않습니다. 새 태그는 기존 태그로 의미를 표현할 수 없을 때만 추가합니다.

## 6. 글 유형별 구성

### Research

```markdown
# 제목

## 요약
## 문제 정의
## 가설
## 실험 환경
## 방법론
## 결과
## 결과 해석
## 한계
## 실무 적용 가능성
## 참고 자료
```

다음 내용을 분명히 구분합니다.

- 기존 연구가 주장한 내용
- 직접 세운 가설
- 직접 측정한 결과
- 결과에 대한 개인적 해석

정량 결과에는 데이터, 모델, 하드웨어, 파라미터와 평가 방법을 함께 기록합니다.

### Paper Reviews

```markdown
# 논문명

## 3줄 요약
## 논문이 해결하는 문제
## 기존 방법의 한계
## 핵심 아이디어
## 모델 구조 또는 알고리즘
## 주요 수식
## 실험 결과
## 잘한 점
## 한계와 의문점
## 실무 적용 가능성
## 관련 연구와 연결점
## 원문 정보
```

논문 리뷰 원칙:

- 초록만으로 작성하지 않고 본문의 방법론과 실험을 확인합니다.
- 논문의 주장과 리뷰어의 의견을 구분합니다.
- 수치와 표는 원문의 조건을 함께 설명합니다.
- 자동 생성 초안은 사실, 수식, 저자, 발표 시점과 링크를 직접 검수한 뒤 공개합니다.
- 원문 그림은 라이선스를 확인하고 출처를 명시합니다.

### Engineering

```markdown
# 문제 또는 기술 주제

## 상황
## 증상
## 원인
## 검토한 대안
## 적용한 해결 방법
## 핵심 코드
## 검증 결과
## 주의사항
## 재사용 체크리스트
```

완성된 코드 전체보다 문제를 이해하는 데 필요한 최소 코드만 제시합니다. 명령어와 코드는 독자가 재현할 수 있는 수준으로 작성합니다.

### Learning Series

각 글 상단에 전체 시리즈와 현재 진행 위치를 표시합니다.

```markdown
## Series

- [x] 1. 모델 선정과 환경 구축
- [x] 2. 아키텍처 분석
- [ ] 3. 데이터 전처리
- [ ] 4. Fine-tuning
- [ ] 5. 평가와 서빙
```

이전 글에서 설명한 내용을 반복하기보다 링크로 연결하고, 각 편이 하나의 명확한 질문에 답하도록 구성합니다.

## 7. 이미지와 다이어그램

이미지는 컬렉션과 글 slug에 맞춰 저장합니다.

```text
assets/images/<collection>/<slug>/
```

Markdown에서는 `site.baseurl`을 사용합니다.

```markdown
![이미지가 전달하는 내용]({{ site.baseurl }}/assets/images/engineering/example/architecture.png)
```

운영 원칙:

- `image.png`, `스크린샷 1.png` 같은 이름 대신 의미 있는 영문 파일명을 사용합니다.
- 모든 이미지에 내용을 설명하는 대체 텍스트를 작성합니다.
- 원문 이미지에는 논문명, Figure 번호와 링크를 명시합니다.
- 내부 시스템 주소, 고객명, 개인정보, API 키가 보이는 캡처는 사용하지 않습니다.
- 구조 설명은 가능하면 Mermaid로 작성하고 해당 글에 `mermaid: true`를 설정합니다.

## 8. 코드와 보안

- 회사·고객의 비공개 소스 코드를 복사하지 않습니다.
- API 키, 토큰, 내부 IP, 이메일, 파일 시스템 경로를 제거합니다.
- 예제 데이터에는 가상 이름과 값을 사용합니다.
- 코드가 특정 버전에 의존하면 라이브러리와 모델 버전을 기록합니다.
- 실행하지 않은 코드를 실행 가능한 예제로 단정하지 않습니다.
- NDA 대상 프로젝트는 기술 원리를 일반화하여 설명합니다.

## 9. 문체

- 첫 문단에서 글이 해결하는 문제와 독자가 얻게 될 내용을 설명합니다.
- 불필요한 수식어보다 조건, 원인, 결과를 구체적으로 작성합니다.
- 전문 용어는 처음 등장할 때 한국어 의미를 함께 설명합니다.
- 연구 결과를 과장하지 않고 적용 조건과 한계를 함께 기록합니다.
- 이모지는 목차 구분을 위해 반복적으로 사용하지 않습니다.
- 제목 체계는 `#` 하나, 주요 절은 `##`, 하위 절은 `###`로 유지합니다.

## 10. 출처와 인용

- 논문은 제목, 저자, 학회 또는 저장소, 연도와 원문 링크를 기록합니다.
- 공식 문서와 원 논문을 우선 인용합니다.
- 직접 인용은 짧게 사용하고 나머지는 자신의 언어로 설명합니다.
- 외부 코드나 그림을 수정했을 때도 원출처와 라이선스를 표시합니다.
- 사실과 개인적인 추론을 문장 안에서 명확히 구분합니다.

## 11. 공개 전 체크리스트

### 콘텐츠

- [ ] 제목과 description만 읽어도 글의 범위를 이해할 수 있다.
- [ ] 주장과 수치에 근거 또는 측정 조건이 있다.
- [ ] 직접 실험한 내용과 인용한 내용을 구분했다.
- [ ] 결과의 한계와 적용 조건을 적었다.
- [ ] 링크와 이미지가 실제 경로에 존재한다.
- [ ] `INSERT_*`, `TODO`, placeholder가 남아 있지 않다.

### 메타데이터

- [ ] Front Matter가 `---`로 정상적으로 닫혀 있다.
- [ ] 날짜 형식이 `YYYY-MM-DD`이다.
- [ ] category와 저장 컬렉션이 일치한다.
- [ ] 태그가 표준 표기를 사용한다.
- [ ] Mermaid가 있는 글만 `mermaid: true`이다.

### 보안과 품질

- [ ] 개인정보, 고객명, 내부 IP와 비밀 값이 없다.
- [ ] 회사 소스 코드나 NDA 자료가 포함되지 않았다.
- [ ] 논문 저자, 연도, 수식과 성능 수치를 원문과 대조했다.
- [ ] 이미지 라이선스와 출처를 확인했다.
- [ ] 로컬 빌드에서 오류가 없고 모바일에서도 읽을 수 있다.

## 12. 로컬 확인

```bash
bundle install
bundle exec jekyll serve
```

브라우저에서 다음 항목을 확인합니다.

- 사이드바에 새 글이 올바른 영역으로 표시되는가
- 글 제목, 목차와 코드 블록이 정상적으로 보이는가
- 내부 링크와 이미지가 열리는가
- Mermaid와 수식이 정상적으로 렌더링되는가
- 긴 표와 코드가 모바일 폭을 벗어나지 않는가

## 13. 자동 발행

학습 초안을 발행할 때 사용할 수 있습니다.

```bash
python .gemini/skills/study-publisher/scripts/publish_study.py \
  --source /path/to/draft.md \
  --collection papers
```

시리즈 글은 시리즈 slug를 함께 전달합니다.

```bash
python .gemini/skills/study-publisher/scripts/publish_study.py \
  --source /path/to/draft.md \
  --collection series \
  --series qwen-image-training
```

자동 생성이나 자동 이동은 공개 승인을 의미하지 않습니다. 게시 전 체크리스트를 따라 사람이 직접 검수합니다.
