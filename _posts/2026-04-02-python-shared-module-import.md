---
title: "Python 프로젝트 간 공통 모듈 공유하기: 패키지 설치와 direnv 비교"
description: "여러 Python 프로젝트에서 공통 모듈을 가져올 때 사용할 수 있는 패키지 설치 방식과 direnv·PYTHONPATH 방식의 장단점을 비교합니다."
date: 2026-04-02 09:00:00 +0900
categories:
  - Engineering Notes
  - Python
tags:
  - Python
  - Packaging
  - direnv
  - PYTHONPATH
toc: true
---

여러 Python 프로젝트에서 공통 유틸리티를 공유하다 보면 실행 중인 프로젝트 바깥에 있는 모듈을 가져와야 하는 경우가 생긴다.

이때 다음 두 가지 방법으로 해결할 수 있다.

1. 공통 모듈을 정식 패키지로 설치하는 방법
2. `direnv`를 이용해 프로젝트별 `PYTHONPATH`를 설정하는 방법

## 예제

다음과 같이 애플리케이션 `function_a`와 공통 모듈 `lib`이 동일한 프로젝트 루트 아래에 있다고 가정해보자.

```text
project/
├── function_a/
│   ├── src/
│   │   ├── clients/
│   │   │   └── n1_clients.py
│   │   └── ...
│   └── services/
│       └── ...
└── lib/
    ├── utils/
    │   ├── preprocess.py
    │   └── file_utils.py
    ├── common/
    └── ...
```


그리고 `function_a/src/clients/n1_clients.py`에서

```python
from lib.utils.file_utils import function_name
```

위의 공통 함수를 가져와 활용하려고 하면, 현 상태에서는 해당 공통 모듈을 인지하지 못한다.


## 왜 인지하지 못할까?

Python은 모듈을 import할 때 `sys.path`에 등록된 경로만 탐색한다.

`function_a`를 작업 디렉터리로 실행하면 상위의 `project/`는 기본 검색 경로에 포함되지 않을 수 있다.

따라서, `lib/`에 `__init__.py`만 추가한다고 해서 모든 실행 환경에서 import가 해결되는 것은 아니다.

`lib`을 포함하는 상위 경로가 `sys.path`에 들어가거나, `lib`이 현재 Python 환경에 패키지로 설치되어야 한다.


## 해결 방법

### 방법 1. 공통 모듈을 패키지로 설치

공통 모듈을 **여러 프로젝트에서 지속해서 사용**한다면 가장 권장하는 방식이다.

IDE, 테스트 러너, CLI와 운영 환경에서 동일한 import 규칙을 사용할 수 있다.


#### 패키지 구조

```text
project/
├── pyproject.toml
├── function_a/
│   ├── src/
│   │   └── clients/
│   │       └── n1_clients.py
│   └── services/
│       └── ...
└── lib/
    ├── __init__.py
    ├── utils/
    │   ├── __init__.py
    │   ├── preprocess.py
    │   └── file_utils.py
    └── common/
        └── __init__.py
```

`__init__.py`의 정확한 파일명에는 밑줄이 앞뒤로 두 개씩 들어간다.


#### pyproject.toml

```toml
[build-system]
requires = ["setuptools>=68"]
build-backend = "setuptools.build_meta"

[project]
name = "project-common-lib"
version = "0.1.0"
requires-python = ">=3.10"

[tool.setuptools.packages.find]
where = ["."]
include = ["lib*"]
```

개발 환경에서는 editable mode로 설치한다.

```bash
cd /path/to/project
python -m pip install -e .
```

설치 후에는 작업 디렉터리와 관계없이 동일하게 import할 수 있다.

```python
from lib.utils.file_utils import function_name
```

다만 예시에서 보이는 `lib`은 다른 패키지와 충돌하기 쉬운 이름이므로, 신규 공통 패키지를 설계할 경우 `project_common`처럼 고유한 import 이름을 사용하는 편이 좋다.

| 장점 | 단점 |
|---|---|
| - 실행 위치에 영향을 덜 받는다. <br/> - IDE와 테스트 도구가 모듈을 안정적으로 인식한다.  <br/> - 의존성과 버전을 명시할 수 있다. <br/> - 배포 및 CI 환경에서 재현하기 쉽다. | - `pyproject.toml`과 버전 관리가 필요하다. <br/> - 작은 프로젝트에서는 초기 구성이 부담스러울 수 있다. |



### 방법 2. direnv로 PYTHONPATH 설정

별도 패키지로 분리하기에는 규모가 작거나, 로컬 개발 단계에서 빠르게 공통 코드를 연결해야 할 때 사용할 수 있다.

`direnv`는 특정 디렉터리에 진입할 때 `.envrc`에 정의한 환경변수를 자동으로 적용하고, 디렉터리에서 벗어나면 원래 환경으로 복원한다.

#### .envrc 작성

`function_a/`에 `.envrc`를 생성한다.

```bash
cd /path/to/project/function_a
```

`.envrc`:

```bash
export PYTHONPATH="$(cd .. && pwd):${PYTHONPATH:-}"
```

설정을 승인한다.

```bash
direnv allow
```

이 설정은 `function_a`의 상위 경로인 `project/`를 `PYTHONPATH`에 추가한다. 

따라서 Python이 `project/lib/`를 찾을 수 있다.

```python
from lib.utils.file_utils import function_name
```

설정 결과는 다음 명령으로 확인할 수 있다.

```bash
python -c "import sys; print('\n'.join(sys.path))"
```

| 장점 | 단점 |
|---|---|
| - 프로젝트 소스 코드를 수정하지 않는다. <br/> - 디렉터리별로 환경변수를 자동 적용한다. <br/> - 로컬 개발 환경을 빠르게 구성할 수 있다. | - 개발자와 실행 서버에 `direnv`가 설치되어 있어야 한다. <br/> - IDE가 셸의 환경변수를 상속하지 않으면 별도 설정이 필요할 수 있다. <br/> - CI, Docker 및 운영 환경에는 같은 경로 설정을 별도로 적용해야 한다. <br/> - `.envrc`를 승인하지 않으면 설정이 활성화되지 않는다. |



## 피해야 할 방법

애플리케이션 코드에서 직접 `sys.path`를 변경하는 방식은 가급적 피한다.

```python
import sys

sys.path.append("/absolute/path/to/project")
```

이 방식은 개인별 절대 경로가 코드에 들어가고, 실행 환경에 따라 동작이 달라진다. 

테스트와 배포 환경에서 경로 문제를 재현하기도 어렵다.

불가피하게 경로를 조정해야 한다면 애플리케이션 코드보다 실행 스크립트, 컨테이너 설정 또는 CI 환경변수에서 관리하는 편이 낫다.

---

## 선택 기준

| 상황 | 권장 방법 |
|---|---|
| 여러 프로젝트에서 장기간 공통 모듈을 사용 | 패키지로 구성한 뒤 editable install |
| CI·Docker·운영 환경에서도 사용 | 패키지 설치 |
| 로컬 PoC 또는 단기 실험 | `direnv`와 `PYTHONPATH` |
| 개인별 절대 경로를 코드에 추가 | 권장하지 않음 |

---

## 결론

공통 코드가 프로젝트의 정식 의존성이라면 패키지로 만들어 설치하는 방식이 가장 안정적이다.

`direnv`는 패키징 비용이 부담스러운 초기 개발 단계에서 유용하지만, 운영 환경까지 확장할 때는 설치 가능한 패키지 구조로 전환하는 것이 좋다.

어떤 방식을 선택하더라도 Python 코드 내부에 개인별 절대 경로를 하드코딩하지 않고, 로컬·테스트·CI·운영 환경에서 동일한 import 규칙을 유지하는 것이 중요하다.
