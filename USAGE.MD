# jinleey126.github.io 사용 설명서

이 저장소는 **Jekyll** 기반의 블로그로, **jekyll-gitbook** 테마를 사용하여 GitBook 스타일의 UI를 제공합니다. GitHub Pages(`https://jinleey126.github.io`)를 통해 호스팅됩니다.

## 1. 프로젝트 주요 디렉토리 및 파일
- `_posts/`: 블로그 포스트(Markdown) 파일들이 저장되는 곳입니다. 파일 이름 규칙: `YYYY-MM-DD-title.md`
- `_pages/`: About, Contact 등의 고정 페이지 관리 디렉토리입니다.
- `_includes/`: 헤더, 푸터, 댓글창 등 재사용 가능한 HTML 조각들이 위치합니다.
- `_layouts/`: 페이지의 기본 레이아웃(home, post, search 등) 템플릿입니다.
- `assets/`: 이미지, 스타일시트(CSS), 자바스크립트(JS) 등 정적 파일들이 저장됩니다.
- `_config.yml`: 사이트의 제목, 설명, URL, 테마 설정 등 전반적인 구성을 관리하는 핵심 파일입니다.
- `Gemfile`: 프로젝트 실행에 필요한 Ruby 라이브러리(Jekyll 및 플러그인)를 정의합니다.

## 2. 로컬 개발 환경 실행 방법
로컬에서 수정 사항을 실시간으로 확인하려면 다음 과정을 따릅니다. (Ruby 설치 필요)

1. **의존성 라이브러리 설치:**
   ```bash
   bundle install
   ```

2. **로컬 서버 실행:**
   ```bash
   bundle exec jekyll serve
   ```
   서버가 구동되면 브라우저에서 `http://localhost:4000` 접속을 통해 미리볼 수 있습니다. `regenerate: true` 설정으로 파일 수정 시 자동 빌드됩니다.

## 3. 새로운 포스트 작성 가이드
1. `_posts/` 디렉토리에 `2026-06-06-new-post.md` 형식의 파일을 생성합니다.
2. 파일 최상단에 다음과 같은 **YAML Front Matter**를 작성해야 Jekyll이 올바르게 인식합니다:
   ```markdown
   ---
   title: 포스트 제목
   author: 작성자 이름
   date: 2026-06-06
   category: Jekyll (또는 다른 카테고리)
   layout: post
   mermaid: true (다이어그램 사용 시)
   ---
   ```
3. 이후 내용은 일반적인 Markdown 문법으로 작성합니다.

## 4. 주요 커스터마이징
- **사이트 정보 수정:** `_config.yml` 파일에서 `title`, `author`, `description` 등을 변경합니다.
- **스타일 변경:** `assets/gitbook/custom.css` 파일에서 원하는 CSS 스타일을 추가하거나 수정할 수 있습니다.
- **특수 블록 사용:** 팁이나 경고 문구를 강조하려면 다음과 같이 작성합니다:
  ```markdown
  > ##### TIP
  > 내용...
  {: .block-tip }
  ```

## 5. 특징 및 플러그인
- **Full-text search:** 내장된 검색 기능을 지원합니다.
- **Mermaid support:** 포스트 상단에 `mermaid: true`를 설정하여 다이어그램을 렌더링할 수 있습니다.
- **TOC (Table of Contents):** `_config.yml`의 `toc` 설정을 통해 문서 내 목차를 자동으로 생성합니다.
