---
title: "ASTOR: Benchmarking and Improving Autoformulation for Soft-Constraint Optimization with a Formal Grammar"
description: "자연어 기반 소프트 제약 최적화 문제의 수식화 오류를 줄이기 위해 형식 문법 기반의 AST 추론 및 결정론적 컴파일 프레임워크와 SoftOR 벤치마크를 제안한 연구"
date: 2024-10-30 09:00:00 +0900
categories:
  - Paper Reviews
  - optimization
paper_authors:
  - Amer Goel
  - Yeganeh Alimohammadi
  - Andrew Daw
paper_url: "https://arxiv.org/pdf/2610.26819v1"
tags:
  - Operations Research
  - Autoformulation
  - Formal Grammar
  - Large Language Models
  - Soft Constraints
toc: true
mermaid: false
---

## 3줄 요약
1. 자연어 의사결정 문제에서 반드시 지켜야 하는 Hard constraint와 위반 패널티를 갖는 Soft constraint를 함께 다루는 **SoftOR** 벤치마크를 제안함.
2. LLM이 직접 최적화 코드를 생성할 때 발생하는 구문 오류 및 수식 불일치를 방지하기 위해, 형식 문법(Formal Grammar)을 통해 Abstract Syntax Tree(AST)를 생성하고 이를 실행 가능한 수리계획 모델로 결정론적으로 컴파일하는 **ASTOR** 프레임워크를 개발함.
3. 실험 결과, ASTOR는 SoftOR 벤치마크에서 단일 프롬프트 및 Multi-agent LLM 기법 대비 가장 높은 정답률(Accuracy)을 기록하며 기존 Hard constraint 전용 벤치마크에서도 우수한 성능을 입증함.

---

## 논문이 해결하는 문제
현실 세계의 운영 연구(Operations Research, OR) 및 의사결정 최적화 문제는 두 가지 상이한 성격의 제약 조건을 포함합니다.
- **Hard Constraints**: 자원의 물리적 한계, 안전 규격 등 절대적으로 위반될 수 없는 제약.
- **Soft Constraints**: 관리자/소비자의 선호도, 권장 납기일 등 위반이 허용되나 목적함수에서 페널티(penalty cost)로 정량화되는 제약.

최근 LLM을 활용해 자연어로 기술된 문제를 실행 가능한 수학적 최적화 코드(Pyomo, Gurobi 등)로 변환하는 **Autoformulation** 연구가 활발히 진행되고 있으나, 대다수의 기존 연구와 벤치마크(NL4Opt, OptBench 등)는 Hard constraint 위주로 구성되어 있어 현실적인 소프트 제약 수식화 문제를 제대로 평가하거나 해결하지 못했습니다. 특히 LLM은 소프트 제약 모델링 시 필요한 슬랙 변수(slack/surplus variables)의 도입 및 목적함수 가중치 스칼라화(scalarization) 과정에서 문맥 누락이나 문법적 결함을 빈번하게 유발합니다.

---

## 기존 방법의 한계
1. **직접 코드 생성(Direct Code Generation)의 환각과 구문 결함**:
   - LLM이 자연어에서 직접 Python 최적화 코드(예: `pyomo.environ` 스크립트)를 생성할 경우, 인덱스 불일치, 정의되지 않은 결정 변수 참조, 제약식 바운드 누락 등 비구문적(semantic) 및 구문적(syntactic) 런타임 오류가 누적됩니다.
2. **소프트 제약 모델링 실패**:
   - 자연어 표현에서 선호도("가급적 X는 Y를 넘지 않아야 한다")를 만났을 때, 이를 완화하기 위한 보조 변수($s^+, s^-$)를 정의하고 목적함수에 목적 가중치(penalty weight)를 부여하는 구조적 변환을 일관되게 수행하지 못합니다.
3. **벤치마크의 편향**:
   - 표준 벤치마크 데이터셋은 대부분 순수 Mixed-Integer Linear Programming (MILP)의 등식/부등식 제약에 집중되어 있어, 다목적(multi-objective) 절충 및 페널티 최적화 문제에 대한 평가 체계가 결여되어 있습니다.

---

## 핵심 기여
1. **SoftOR Benchmark 구축**:
   - 관리자, 스케줄링, 공급망 등 실제 비즈니스 도메인의 소프트 제약 및 선호 구조를 반영한 신규 수리계획 벤치마크를 공개함.
2. **ASTOR (Abstract Syntax Tree for Operations Research) 제안**:
   - 도메인 특화 수리계획 형식 문법(Context-Free Grammar 기반 EBNF)을 정의하고, LLM이 이 문법에 부합하는 AST 노드만을 추론하도록 강제한 뒤, 파서와 템플릿 컴파일러를 통해 완전한 최적화 코드로 결정론적 변환(Deterministic Compilation)을 수행하는 파이프라인 설계.
3. **높은 유효 실행률과 최적화 정확도 달성**:
   - SoftOR 및 기존 Hard-constraint 벤치마크 전반에서 유효 코드 실행 비율(Executable Rate)을 극대화하고 목적함수 값 일치도(Optimality Accuracy)를 획기적으로 개선함.

---

## 제안 방법과 주요 수식

### 1. 소프트 제약의 수리적 정식화 (Mathematical Formulation)
일반적인 선형 계획(LP) 및 혼합 정수 계획(MIP)에서 제약 조건은 집합 $I_{hard}$와 $I_{soft}$로 분할됩니다.
결정 변수 벡터를 $x \in \mathbb{R}^n$, 기본 비용 계수를 $c \in \mathbb{R}^n$라 할 때, 표준 정식화는 다음과 같습니다:

$$
\min_{x, s^+, s^-} \quad c^T x + \sum_{i \in I_{soft}} \left( w_i^+ s_i^+ + w_i^- s_i^- \right)
$$

$$
\text{subject to} \quad A_j x \le b_j, \quad \forall j \in I_{hard}
$$

$$
A_i x - s_i^+ + s_i^- = b_i, \quad \forall i \in I_{soft}
$$

$$
s_i^+, s_i^- \ge 0, \quad \forall i \in I_{soft}
$$

$$
x \in \mathcal{X}
$$

- $s_i^+, s_i^-$: 소프트 제약 $i$의 상한 위반(over-achievement) 및 하한 위반(under-achievement)을 나타내는 슬랙/서플러스(slack/surplus) 비음(non-negative) 변수.
- $w_i^+, w_i^-$: 각 위반 단위당 부과되는 페널티 가중치(Penalty weights).

### 2. ASTOR의 형식 문법 (Grammar-guided AST)
ASTOR는 자연어 프롬프트를 입력받아 직접 코드를 내뱉지 않고, 미리 정의된 EBNF(Extended Backus-Naur Form) 스타일의 수리계획 추상 문법 트리를 생성합니다.

문법 생성 규칙의 핵심 구조:
```text
<OptimizationModel> ::= <Variables> <Objectives> <HardConstraints> <SoftConstraints>
<SoftConstraint>    ::= "SOFT_CONSTRAINT" "(" <Expr> , <RelOp> , <Expr> , "penalty=" <PenaltyExpr> ")"
<RelOp>             ::= "<=" | ">=" | "=="
```

LLM의 출력 토큰은 이 문법 규칙에 따른 유효 토큰 집합으로 constrained decoding(인코더-디코더 또는 로그잇 바이어스 제어)을 거쳐 생성되므로, **문법적으로 불가능한 수식이나 정의되지 않은 심볼의 출현이 원천 차단**됩니다.

### 3. 결정론적 컴파일 (Deterministic Compiler)
추론된 AST 노드는 다음과 같은 결정론적 매핑 함수 $\mathcal{C}$를 통해 컴파일됩니다:
- 선언된 결정 변수 집합 $\mathcal{V}$는 백엔드 솔버 인터페이스(예: Gurobi Python API 또는 Pyomo)의 `Var` 객체로 인스턴스화됩니다.
- 각 `<SoftConstraint>` 노드는 자동으로 해당 제약용 슬랙 변수 $s_i \ge 0$를 심볼릭 테이블에 등록하고, 등가 패널티 항 $w_i s_i$를 목적함수 수식 트리에 자동으로 결합(Augmentation)합니다.
- 파싱된 수식 트리는 최종적으로 무결성이 보장된 실행 코드로 렌더링됩니다.

---

## 핵심 구조

```
[Figure 1 Architecture Concept Placeholder]
*원문 논문의 Figure 1(ASTOR Framework Architecture)을 참조하여 캡처를 권장합니다.*
```

> **Figure 1 구조 상세 설명**:
> 원문의 시스템 파이프라인 다이어그램은 크게 **(1) Natural Language Problem Input**, **(2) LLM with Constrained Decoding**, **(3) Grammar-Guided AST Representation**, **(4) Deterministic Symbolic Compiler**, **(5) Executable Solver Code (Pyomo/Gurobi)**의 5단계 흐름을 시각화합니다.
>
> 1. **입력단 (Input Stage)**: Hard 및 Soft constraint(선호 사항, 패널티 문구)가 섞인 자연어 문제 기술서와 도메인 파라미터가 프롬프트 형태로 구성됩니다.
> 2. **추론단 (Constrained LLM Parsing)**: LLM은 자유 형식의 코드가 아닌 정의된 Formal Grammar 규칙 테이블을 참조하여 토큰을 생성합니다. 내부적으로 변수 정의 노드, 목적함수 노드, 하드 제약 노드, 소프트 제약 노드가 순차적으로 분기하는 트리 그래프 구조를 형성합니다.
> 3. **중간 표현 (AST Stage)**: 추출된 AST는 XML/JSON 혹은 중첩 객체 형태의 중간 표현(IR)으로 도출되며, 각 노드는 제약식의 좌변(LHS), 관계 연산자(Op), 우변(RHS), 그리고 소프트 제약 특유의 페널티 속성(Penalty weight / Type)을 명시적인 키-값 쌍으로 보존합니다.
> 4. **컴파일러 (Compiler Engine)**: 컴파일러는 AST를 순회(Tree Traversal)하면서 소프트 제약 노드를 만날 때마다 슬랙 변수를 자동 합성하고, 목적함수 트리에 가중치 합을 선형 결합합니다.
> 5. **출력단 (Code Output)**: 최종적으로 최적화 솔버가 즉시 실행할 수 있는 정제된 스크립트가 도출되어 실행 오류(Syntax Error) 없이 최적해를 도출합니다.

---

## 실험 설정과 결과

### 1. 데이터셋
- **SoftOR (신규)**: 산업 현장의 선호 및 규제 조건을 포함한 다수의 소프트 제약 최적화 문제로 구성.
- **기존 벤치마크**: NL4Opt, OptBench 등 순수 Hard-constraint 중심의 표준 벤치마크.

### 2. 비교 베이스라인
- **Direct Prompting**: GPT-4o, Claude 계열 모델을 통한 Zero-shot / Few-shot 직접 코드 생성.
- **Chain-of-Thought (CoT)**: 단계적 수학 정식화 후 코드 생성.
- **Multi-Agent Frameworks**: 역할 분담(수식화 에이전트, 코드 작성 에이전트, 디버깅 에이전트) 기반 프레임워크.

### 3. 주요 평가 지표
- **Executable Rate (ER)**: 생성된 코드가 런타임 에러 없이 솔버에서 실행 완료되는 비율 (%).
- **Formulation Accuracy (Acc)**: Ground Truth 솔버 결과와 동일한 최적해(Optimal Value) 및 최적해 벡터(Optimal Solution Vector)를 도출한 비율 (%).

### 4. 결과 요약
- SoftOR 데이터셋에서 ASTOR는 기존 Direct Prompting 및 Multi-agent 모델 대비 Formulation Accuracy에서 두드러진 개선을 보였습니다. 특히 기존 LLM들이 소프트 제약 변환 시 슬랙 변수 부호 오류나 목적함수 누락으로 인해 40~50% 수준의 정답률에 머무른 반면, ASTOR는 높은 유효 실행률(Executable Rate > 95%)과 함께 최고 수준의 목적함수 정확도를 달성했습니다.
- Hard 제약 전용 벤치마크에서도 기존 최적화 전용 프레임워크와 대등하거나 소폭 상회하는 성능을 유지하여, 소프트 제약 처리 확장이 일반 최적화 성능을 저하시키지 않음을 검증했습니다.

---

## 잘한 점
1. **문제 정의의 실용성**:
   - 실무 OR 프로젝트에서 가장 골치 아픈 영역인 "완화 가능한 선호 제약(Soft constraint)"을 프롬프트 엔지니어링 수준이 아니라 정형 벤치마크와 체계적 아키텍처로 끌어올림.
2. **Deterministic Compiler를 통한 오류 원천 차단**:
   - LLM에게 솔버 라이브러리(Pyomo/Gurobi API)의 세부 문법까지 맡기지 않고, 고수준의 AST 추론만 전담시킨 뒤 컴파일을 기계적으로 처리함으로써 문법 에러 및 인덱스 참조 에러를 획기적으로 제거함.
3. **확장 가능한 문법 체계**:
   - 정의된 EBNF 문법은 선형 제약뿐만 아니라 향후 비선형, 2차 계획법(QP), 이산 제약으로 확장이 용이한 모듈형 구조를 지님.

---

## 한계와 의문점
1. **복잡한 비선형/조합적 페널티 함수의 처리 한계**:
   - 논문에서 다루는 소프트 제약은 주로 선형 슬랙 및 L1-norm 형태의 페널티에 집중되어 있습니다. 계단형 패널티(stepwise penalty)나 조건부 볼록(piecewise convex) 패널티 등 복잡한 비선형 비용 구조를 문법적으로 완전히 표현하고 컴파일할 수 있는지에 대한 확장이 필요합니다.
2. **도메인 특화 문법의 유연성 한계**:
   - LLM이 자연어로부터 정보를 추출할 때 사전 정의된 AST 문법 규칙에 정확히 들어맞지 않는 모호한 비즈니스 규칙을 마주했을 경우, 문법 파싱 자체가 실패하거나 fallback 메커니즘이 취약해질 수 있습니다.

---

## 실무 적용 가능성
- **엔터프라이즈 의사결정 지원 시스템(Decision Support Systems)**:
  - 비전문가 현업 관리자가 자연어로 "A 공장의 초과 근무는 가급적 주당 10시간 이내로 제한하되 필요시 시간당 5만 원 페널티를 부여한다"와 같이 입력했을 때, 사내 수리계획 솔루션으로 안전하게 변환하는 인터페이스로 즉시 적용 가능.
- **LLM 에이전트의 Optimization Tool 신뢰성 제고**:
  - 에이전트 파이프라인에서 솔버 툴을 호출할 때 파이썬 코드를 통째로 실행(Eval)하는 위험한 방식 대신, AST 검증을 거치는 안전한 샌드박스형 수식화 레이어로 도입 가능.

---

## 관련 연구와 연결점
- **NL4Opt / OptBench**: LLM 기반 자연어-최적화 모델 정식화 벤치마크.
- **Grammar-Guided Constrained Decoding (Grammar-based Decoding)**: Outlines, Guidance, GBNF 등 LLM 출력의 구조적 무결성을 보장하는 디코딩 기술과의 접목.
- **Goal Programming & Multi-Criteria Optimization**: 다목적/선호 최적화 이론을 LLM Autoformulation 파이프라인에 체계화한 선행 연구와의 연속선상에 위치.

---

## 원문 정보
- **Title**: ASTOR: Benchmarking and Improving Autoformulation for Soft-Constraint Optimization with a Formal Grammar
- **Authors**: Amer Goel, Yeganeh Alimohammadi, Andrew Daw
- **Venue/Repository**: arXiv
- **Published**: 2024 (arXiv preprint)
- **URL**: [https://arxiv.org/pdf/2610.26819v1](https://arxiv.org/pdf/2610.26819v1)

> 이 글은 자동 생성된 초안을 바탕으로 작성되며, 공개 전에 저자·수식·수치·출처를 직접 검수합니다.