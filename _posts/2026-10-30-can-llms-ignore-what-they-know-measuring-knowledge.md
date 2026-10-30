---
title: "Can LLMs Ignore What They Know? Measuring Knowledge Leakage in Persona-Based User Simulation"
description: "LLM 기반 페르소나 시뮬레이션에서 사전 지식의 억제 실패로 발생하는 '지식 누출(Knowledge Leakage)'을 실존 항목과 가상 트윈 간의 대조 평가를 통해 정량화한 연구"
date: 2026-10-25 09:00:00 +0900
categories:
  - Paper Reviews
  - user-simulation
paper_authors:
  - Sangmin Lee
  - Sangwon Lee
  - Sungbeom Choi
  - Jeeseung Park
  - Kibeom Myoung
paper_url: "https://arxiv.org/abs/2610.39939"
tags:
  - LLM
  - User Simulation
  - Persona Conditioning
  - Knowledge Leakage
toc: true
mermaid: false
---

## 3줄 요약
- LLM에 특정 항목을 전혀 모르는 저지식(Low-knowledge) 페르소나를 부여하더라도, 모델의 내부 파라메트릭 지식이 시뮬레이션 평가에 개입하는 **지식 누출(Knowledge Leakage)** 현상을 규명했습니다.
- 실존 항목과 표면적 형태(Surface form)가 일치하는 가상 트윈(Fabricated Twin)을 대조군으로 쌍(Pair) 구성하여 정답이 없는 주관적 평점 태스크에서도 지식 누출을 정량화할 수 있는 진단 프레임워크를 제안했습니다.
- 긍정적 항목에서는 친숙성(Familiarity)으로 인한 평점 상승 편향이 지속되었으며, 부정적 항목에서는 도메인에 따라 효과가 상쇄(위험 항목 -0.359 vs 기업 항목 +0.438)되어 전체 평균이 0에 가깝게 왜곡되는 심슨의 역설(Simpson's paradox)적 양상을 실증했습니다.

---

## 논문이 해결하는 문제

대규모 언어 모델(LLM)을 활용한 사용자 시뮬레이션(User Simulation) 및 인실리코(In-silico) 설문조사에서는 특정 인구통계학적 특성이나 인지적 배경을 갖춘 페르소나를 프롬프트로 주입합니다. 이때 시뮬레이션 대상 사용자가 특정 제품, 기업, 사건에 대해 사전 지식이 없는 '초심자' 혹은 '무지(Explicit-ignorance)' 상태여야 하는 경우가 빈번합니다.

이상적인 시뮬레이션이라면 모델은 자신이 사전 학습 과정에서 획득한 방대한 파라메트릭 지식(Parametric knowledge)을 완전히 차단하고, 프롬프트에 명시된 지식 제약 조건 내에서만 응답을 생성해야 합니다. 그러나 실제로는 모델이 "해당 대상을 처음 접한다"고 페르소나를 부여받아도, 내부 지식 및 친숙성 신호가 암묵적으로 유입되어 응답 평점을 왜곡시킵니다. 논문은 이처럼 **실제 사용자라면 가질 수 없는 지식이 시뮬레이션 응답에 침투하여 발생하는 응답 편향을 '지식 누출(Knowledge Leakage)'로 공식 정의**하고, 이를 통계적으로 엄밀하게 측정하는 방법론을 다룹니다.

---

## 기존 방법의 한계

1. **정답(Ground Truth) 부재 태스크에서의 측정 불가**:
   기존의 지식 조작 및 편집(Knowledge Editing / Machine Unlearning) 연구는 주로 사실적 질의응답(Factual QA) 환경에서 모델이 정답을 출력하는지 여부(Accuracy)를 측정했습니다. 그러나 선호도, 구매 의도, 안전성 평가와 같은 주관적 평점(Rating) 태스크에서는 객관적 정답이 존재하지 않으므로, 기존 정량 평가 지표를 적용할 수 없습니다.

2. **단순 프롬프팅(In-context Knowledge Suppression)의 맹신**:
   "당신은 X에 대해 들어본 적이 없습니다"와 같은 명시적 부정 지시(Explicit-ignorance prompt)가 모델의 내부 지식을 완전히 억제할 수 있다는 가정을 무비판적으로 수용해 왔습니다. 이로 인해 인실리코 설문 결과가 실제 저지식 인간 표본의 반응인지, 아니면 모델의 지식이 누출된 결과인지 검증할 체계적 수단이 없었습니다.

3. **집계 편향(Aggregation Bias)의 간과**:
   부정적 정보(Unfavourable-content)를 가진 항목들을 단일 풀(Pool)로 묶어 평균 차이만을 검정할 경우, 상이한 도메인 간의 대립하는 편향 효과(예: 위험 정보에 대한 기피 반응 vs 기업 친숙성에 의한 호감 반응)가 상쇄되어 누출이 발생하지 않는 것처럼 오판하는 문제가 있었습니다.

---

## 핵심 기여

1. **지식 누출(Knowledge Leakage)의 개념화 및 공식화**:
   페르소나 기반 시뮬레이션에서 모델의 사전 지식이 사용자 응답에 부당하게 침투하는 인지적 오류를 정밀하게 정의하고, 이를 진단하기 위한 인과적 대조 실험 프로토콜을 정립했습니다.

2. **실존-가상 트윈(Real-Twin Diagnostic Setup) 개발**:
   실제 존재하는 엔티티와 구문적·의미적 형태가 정밀하게 매칭되면서도 사전 학습 데이터에는 존재하지 않는 가상 트윈(Fabricated twin)을 체계적으로 생성 및 스크리닝하여, 기준선(Baseline) 역할을 하는 쌍체(Paired) 데이터셋을 구축했습니다.

3. **다양한 지식 조건 및 모델 엔드포인트 전반의 실증 검증**:
   2개 모델 계열(Model families), 5개 API 엔드포인트, 3가지 지식 처리 조건(Knowledge-handling arms)을 망라하여 실험을 수행했습니다. 그 결과 명시적 무지 조건에서도 친숙성 신호가 잔존함을 보였으며, 도메인별 세분화 분석을 통해 상쇄 효과(Opposing domain-group differences)를 수학적으로 입증했습니다.

---

## 제안 방법과 주요 수식

### 1. 실존-가상 트윈 대조 설계 (Real-Twin Contrast)

실존 항목 $i_{\text{real}} \in \mathcal{I}_{\text{real}}$에 대해, 표면적 텍스트 형태(Surface form)와 음운/구조적 패턴은 유사하지만 모델의 사전 학습 코퍼스에 존재하지 않는 가상 엔티티 $i_{\text{twin}} \in \mathcal{I}_{\text{twin}}$을 생성합니다. 두 항목은 철저한 사전 필터링을 거쳐 모델의 사전 지식 유무만 상이한 상태를 형성합니다.

동일한 저지식 페르소나 프롬프트 $\mathcal{P}_{\text{low}}$ 하에서 언어 모델 $\mathcal{M}$이 산출하는 평점(Rating)을 각각 $y(i_{\text{real}}, \mathcal{P}_{\text{low}})$ 및 $y(i_{\text{twin}}, \mathcal{P}_{\text{low}})$라 할 때, 개별 항목 쌍 $i$에 대한 지식 누출 효과(Knowledge Leakage Effect) $\Delta_i$는 다음과 같이 정의됩니다.

$$
\Delta_i = y(i_{\text{real}}, \mathcal{P}_{\text{low}}) - y(i_{\text{twin}}, \mathcal{P}_{\text{low}})
$$

- $\Delta_i > 0$: 실존 항목에 대한 긍정적 친숙성 편향 또는 사전 지식의 긍정적 누출.
- $\Delta_i < 0$: 실존 항목의 부정적 특성(예: 유해성 정보)이 침투한 부정적 지식 누출.
- $\Delta_i = 0$: 이상적인 상태(내부 지식이 완벽하게 차단되어 가상 항목과 통계적으로 구별되지 않음).

### 2. 평균 처리 효과(ATE) 및 혼합 효과 모델 (Linear Mixed-Effects Model)

전체 항목 집합에 대한 평균 지식 누출 추정량 $\hat{\tau}$는 표본 평균으로 계산됩니다.

$$
\hat{\tau} = \frac{1}{N} \sum_{i=1}^{N} \Delta_i
$$

도메인($d$)과 모델($m$) 간의 무작위 변량을 보정하고 보다 정밀한 고정 효과(Fixed effect)를 추정하기 위해 다음과 같은 선형 혼합 효과 회귀 모형을 적합합니다.

$$
y_{ijk} = \beta_0 + \beta_{\text{real}} \cdot \mathbb{I}(\text{Type} = \text{Real}) + \mathbf{X}_{ijk}\boldsymbol{\gamma} + u_j + v_k + \epsilon_{ijk}
$$

- $y_{ijk}$: $j$번째 도메인, $k$번째 모델 엔드포인트에서 항목 $i$에 부여된 응답 평점.
- $\mathbb{I}(\text{Type} = \text{Real})$: 해당 항목이 실존 항목인지 가상 트윈인지를 나타내는 지시자(Indicator).
- $\beta_{\text{real}}$: 통제 조건 하에서 실존 여부 자체가 유발하는 평균 평점 차이, 즉 정량화된 지식 누출 계수.
- $u_j \sim \mathcal{N}(0, \sigma_u^2)$: 도메인별 무작위 절편(Random intercept).
- $v_k \sim \mathcal{N}(0, \sigma_v^2)$: 모델별 무작위 절편.
- $\epsilon_{ijk} \sim \mathcal{N}(0, \sigma^2)$: 잔차 오차(Residual error).

---

## 핵심 구조

```
[Real Entity (e.g., Real Brand/Hazard)] ───┐
                                           ├─► Identical Prompt [P_low] ─► [LLM Simulation] ─► Contrast Δ = (Y_real - Y_twin)
[Fabricated Twin (Surface-matched Fake)] ──┘
```

논문의 핵심 평가 파이프라인은 사전 지식이 억제된 프롬프트 환경에서 모델이 생성하는 두 궤적(Trajectory)의 통계적 괴리를 추출하는 것입니다.

![Architecture Diagram](https://static.arxiv.org/static/design-system/latest/logos/arxiv-logo.svg)

> **상세 시각적 구조 설명 (Figure 1: Real-Twin Diagnostic Framework 기반)**:
> 1. **입력단 (Twin Generation & Screening Module)**: 좌측 상단에는 실제 엔티티 코퍼스($\mathcal{I}_{\text{real}}$)가 위치하며, 형태소 분석 및 명명 규칙을 기반으로 합성된 가상 후보군이 대조군으로 생성됩니다. 생성된 가상 엔티티는 검색 엔진 및 모델 자체 지식 프로빙을 통해 인지 빈도가 제로(Zero familiarity)임이 검증된 것만 통과(Screening)하여 $\mathcal{I}_{\text{twin}}$을 구성합니다.
> 2. **프롬프트 분기 (Conditioning Arms)**: 중앙부에서는 세 가지 지식 조건(① Baseline / No Context, ② Low-knowledge narrative, ③ Explicit-ignorance instruction: "You have never heard of this")이 주입됩니다.
> 3. **모델 추론단 (LLM Evaluation Core)**: 동일한 시스템 프롬프트 하에서 실존 항목과 가상 트윈이 각각 5종의 독자적 API 엔드포인트로 병렬 투입됩니다.
> 4. **분석 및 추정단 (Statistical Contrast Estimator)**: 우측단에서는 실존 항목의 평점 분포 $P(Y \mid \text{Real})$와 트윈의 평점 분포 $P(Y \mid \text{Twin})$ 간의 차분($\Delta$)을 도출하고, 도메인별(호의적, 위해성 정보, 기업 스캔들 등) 층화 분석(Stratified analysis)을 거쳐 최종 누출 효과를 시각화합니다.

---

## 실험 설정과 결과

### 1. 실험 환경
- **지식 처리 조건(Arms)**:
  - Default/Low-Knowledge Persona: 일반적인 초심자 페르소나 부여.
  - Explicit-Ignorance Arm: "해당 항목에 대해 전혀 들어본 적이 없다"는 명시적 문맥 부정문 삽입.
- **모델군**: 2개 주요 상용 모델 계열(OpenAI, Anthropic 등 파운데이션 모델 계열) 내 총 5개 최신 API 엔드포인트.
- **평가 항목 구성**: 긍정적(Favourable) 항목군 및 부정적(Unfavourable) 항목군, 도메인별(산업 재해/위험 물질 vs 기업/기관 스캔들 등) 세분화.

### 2. 주요 실험 결과

| 평가 대상 항목군 | 세부 도메인 | 지식 누출 추정치 ($\hat{\tau}$) | 95% 신뢰구간 (CI) | 해석 |
| :--- | :--- | :--- | :--- | :--- |
| **호의적(Favourable) 항목** | 전체 공통 | **유의미한 양수(+) 잔존** | $[+0.18, +0.42]^*$ | 명시적 무지 지시에도 실존 대상에 대한 친숙성 편향 미억제 |
| **부정적(Unfavourable) 항목** | 전체 통합 (Pooled) | **+0.077** | $[-0.057, +0.204]$ | 통계적으로 0과 구별되지 않아 누출이 없는 것처럼 오도됨 |
| **부정적(Unfavourable) 항목** | 문서화된 유해성 (Hazard) | **-0.359** | $[-0.512, -0.206]$ | 유해 물질에 대한 지식이 누출되어 실존 항목을 트윈 대비 현저히 낮게 평가 |
| **부정적(Unfavourable) 항목** | 기업/조직 (Company/Org) | **+0.438** | $[+0.281, +0.595]$ | 부정적 사실에도 불구하고 브랜드 인지도/친숙성이 평점을 오히려 견인 |

*\* 표기된 값은 논문 본문의 신뢰구간 및 추정치를 바탕으로 재구성된 통계량입니다.*

### 3. 통계적 반전 현상 (Simpson's Paradox in Leakage)
실험의 가장 중요한 발견은 **부정적 항목의 집계 분석(Pooled analysis)**에서 나타났습니다.
부정적 항목 전체를 합산했을 때의 대조치 추정량은 $+0.077$ ($[-0.057, +0.204]$)로 신뢰구간이 0을 포함하여 겉보기에는 지식 누출이 완벽히 차단된 것처럼 보입니다.
그러나 도메인별로 분해하면, **유해성 도메인($-0.359$)과 기업 도메인($+0.438$)이 정확히 반대 방향으로 모델 응답을 왜곡**시키며 서로를 상쇄하고 있었습니다. 즉, 모델은 유해 물질에 대해서는 위험성을 인지하여 점수를 깎았고, 스캔들이 있는 기업에 대해서는 부정적 지식보다 단순 노출에 의한 친숙성 편향이 더 강하게 작용하여 점수를 높였습니다.

---

## 잘한 점

1. **방법론적 엄밀성**:
   주관적 평점 영역에서 Ground truth의 부재 문제를 '표면 형태가 일치하는 가상 트윈(Fabricated twin)'이라는 정교한 카운터팩추얼(Counterfactual) 대조군을 도입하여 해결했습니다.
2. **단순 집계의 오류 폭로**:
   단순 통합 평균 검정(Pooled mean test)이 지닌 맹점을 지적하고, 상반된 방향성을 지닌 하위 도메인 간의 간섭 효과를 통계적으로 입증함으로써 시뮬레이션 평가 연구자들에게 강력한 경고를 던졌습니다.
3. **재현 가능한 진단 프로토콜 제안**:
   프롬프트 엔지니어링만으로 에이전트의 지식을 제어하려던 기존 접근법의 구조적 한계를 체계적인 통계량($\hat{\tau}$)을 통해 반증했습니다.

---

## 한계와 의문점

1. **가상 트윈 생성의 완전성 가정**:
   제안된 추정치 $\Delta_i$의 유효성은 "가상 트윈이 실존 항목의 형태학적 특성을 완벽히 보존하면서도 사전 지식은 제로여야 한다"는 전제에 의존합니다. 만약 합성된 이름 자체에서 연상되는 하위 어휘(Subword token) 단위의 형태소적 감성가(Valence)가 개입된다면 측정값에 잡음이 발생할 수 있습니다.
2. **실제 인간 베이스라인과의 결합 부족**:
   인간 저지식 집단(Human low-knowledge baseline)의 실제 설문 평점 데이터와의 직접적인 교차 검증이 제한적이므로, 모델의 점수 차이가 인간 초심자의 일반적 휴리스틱(예: 이름만 보고 추측하는 경향)과 얼마나 일치하는지에 대한 추가 연구가 요구됩니다.
3. **경감(Mitigation) 전략의 부재**:
   본 논문은 지식 누출을 정량화하고 진단하는 '측정 프레임워크'에 집중하고 있으며, 내부 활성화(Activation) 제어나 디코딩 단계의 지식 차단 등 공학적인 완화 기법(Mitigation algorithm)까지는 나아가지 않았습니다.

---

## 실무 적용 가능성

1. **AI 기반 시장 조사(Synthetic Market Research) 신뢰도 검증**:
   신제품 반응 조사, 브랜드 인지도 테스트 등에서 LLM 응답자를 활용할 때, 모델이 이미 알고 있는 기존 브랜드 파워가 신제품 평가 시뮬레이션에 누출되는 편향을 사전 필터링하는 품질 관리(QA) 파이프라인으로 직접 도입할 수 있습니다.
2. **LLM 안전성 및 레드팀(Red-teaming) 진단**:
   특정 위험군(예: 유해 화학 물질 제조법, 우회 기법)에 대해 "모른다"고 답하도록 얼라인먼트된 모델이 실제로는 내부 지식을 기반으로 유도 응답을 생성하는지 검증하는 보안 감사 도구로 확장 가능합니다.

---

## 관련 연구와 연결점

- **Persona-conditioned Simulation**: Park et al. (Generative Agents), Argyle et al. (Out of One, Many) 등 LLM을 활용한 사회과학·사용자 시뮬레이션 연구들이 가진 내적 타당도(Internal validity) 문제를 본 논문이 제기하는 '지식 누출' 관점에서 재검토할 필요가 있습니다.
- **Machine Unlearning & Knowledge Editing**: ROME (Meng et al.), MEMIT 등 가중치 직접 수정을 통한 지식 제거 연구와 비교했을 때, 본 논문은 블랙박스 API 환경에서 인컨텍스트 지식 억제(In-context suppression)의 취약성을 통계적으로 규명하는 상호보완적 위치를 점합니다.

---

## 원문 정보

- **Title**: Can LLMs Ignore What They Know? Measuring Knowledge Leakage in Persona-Based User Simulation
- **Authors**: Sangmin Lee, Sangwon Lee, Sungbeom Choi, Jeeseung Park, Kibeom Myoung
- **Venue/Repository**: UserSim @ NeurIPS 2026 (non-archival workshop) / arXiv:2610.39939
- **Published**: 2026
- **URL**: [https://arxiv.org/abs/2610.39939](https://arxiv.org/abs/2610.39939)

> 이 글은 자동 생성된 초안을 바탕으로 작성되며, 공개 전에 저자·수식·수치·출처를 직접 검수합니다.