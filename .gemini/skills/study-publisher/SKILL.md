---
name: study-publisher
description: Publish a local Markdown draft and its images into the papers, engineering, or series collection of this Jekyll blog.
---

# Study Publisher

블로그 운영 기준은 저장소 루트의 `guideline.md`를 따릅니다.

## Collections

- `_papers/`: 논문 리뷰
- `_engineering/`: 구현과 문제 해결 기록
- `_series/<series-slug>/`: 연속 학습 콘텐츠

## Usage

```bash
python .gemini/skills/study-publisher/scripts/publish_study.py \
  --source /path/to/draft.md \
  --collection papers
```

시리즈:

```bash
python .gemini/skills/study-publisher/scripts/publish_study.py \
  --source /path/to/draft.md \
  --collection series \
  --series qwen-image-training
```

스크립트는 로컬 이미지를 `assets/images/<collection>/<post-slug>/`로 복사하고 링크를 Jekyll 경로로 변경합니다. 자동 발행 후에도 `guideline.md`의 공개 전 체크리스트에 따라 사람이 직접 검수해야 합니다.

