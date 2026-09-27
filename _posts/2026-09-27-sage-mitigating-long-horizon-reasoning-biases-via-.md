---
title: "SAGE: Mitigating Long-Horizon Reasoning Biases via Topological Guidance"
description: "희소 보상 환경에서 발생하는 탐색 편향과 복리 편향을 완화하기 위해 대수적 희소화와 쌍곡 기하학적 유도를 결합한 SAGE 프레임워크를 제안합니다."
date: 2026-09-30 09:00:00 +0900
categories:
  - Paper Reviews
  - llm-reasoning
paper_authors:
  - Xinyue Zeng
  - Jiawei Zhang
  - Yujun Yan
  - Dawei Zhou
paper_url: "https://arxiv.org/abs/2609.30192v1"
tags:
  - Long-Horizon Reasoning
  - Hyperbolic Embedding
  - Symbolic Reasoning
  - Search Guidance
  - Large Language Models
toc: true
mermaid: false
---

## 3줄 요약
- 긴 추론 경로(Long-Horizon Reasoning)에서 대형 언어 모델(LLM)이 겪는 실패 원인을 **국소적 유효성에 의한 탐색 편향(Exploration Bias)**과 **깊이에 따른 오류 누적 편향(Compounding Bias)**으로 공식화함.
- 기호 폐포 분석(Symbolic Closure Analysis, SCA)을 이론적 토대로 삼아, 연산자 기반의 **대수적 희소화(Algebraic Sparsification)**와 **쌍곡 기하 구조 기반 유도(Hyperbolic Structural Guidance)**를 결합한 탐색 프레임워크 **SAGE**를 제안함.
- Andrews-Curtis 추측 등 고난도 기호 수학 및 12개 벤치마크 전반에서 최대 8배의 성능 향상을 기록하며 기하학적·대수적 귀납 편향의 유효성을 입증함.

---

## 논문이 해결하는 문제
대형 언어 모델(LLM)을 활용하여 수학적 증명, 기호 변환, 복잡한 계획 수립과 같은 장기 추론(Long-Horizon Reasoning) 문제를 해결할 때 가장 큰 장애물은 **희소 보상(Sparse Reward)** 환경입니다. 추론 단계가 깊어질수록 상태 공간(State Space)은 지수적으로 폭증하지만, 유효한 보상은 오직 최종 해(terminal state)에만 도달했을 때 단 한 번 주어집니다.

논문은 이러한 환경에서 모델이 겪는 붕괴 현상을 다음 두 가지 구조적 편향(Structural Biases)으로 규명합니다:
1. **탐색 편향 (Exploration Bias)**: 생성 모델이 국소적으로는 문법적·논리적으로 타당해 보이는 분기(Locally Admissible Branches)를 선택하지만, 해당 분기들이 전역적으로는 목표에 도달할 수 없는 구조적 불안정성(Structural Instability)을 지녀 낭비적인 탐색을 유발함.
2. **복리 편향 (Compounding Bias)**: 각 깊이(depth)에서 발생하는 미세한 국소적 오차 및 불확실성이 탐색 깊이가 깊어질수록 기하급수적으로 누적되어 드문 보상(Rare Rewards)을 수렴 신호로부터 차단함.

---

## 기존 방법의 한계
- **Tree-search (MCTS / ToT 등) 기반 방식**: 몬테카를로 트리 탐색(MCTS)이나 Thought-Tree 탐색 기법은 가치 함수(Value Function)나 PRM(Process Reward Model)의 품질에 과도하게 의존합니다. 희소 보상 환경에서는 중간 단계 가치 평가의 분산이 극도로 커져 탐색 편향을 제어하지 못하고 오분기(spurious branches)로 발산합니다.
- **유클리드 공간 기반 임베딩 및 유사도 측정**: 기존 추론 경로 평가 모델들은 유클리드 공간($\mathbb{R}^d$)에 상태를 매핑합니다. 그러나 트리 구조 및 계층적 분기 구조(Hierarchical Branching)의 노드 수는 깊이에 따라 지수적으로 증가하는데, 유클리드 공간의 체적은 다항식($r^d$)으로만 증가하므로 심각한 왜곡(Distortion)이 발생하여 깊이에 따른 복리 편향을 완화하지 못합니다.
- **국소적 규칙 필터링**: 단순히 국소적 문법(Syntax) 검증만 수행하는 필터는 전역적 대수적 구조나 불변량(Invariants)을 감지하지 못해 공허한 루프(Dead-end loop) 탐색을 배제하지 못합니다.

---

## 핵심 기여
1. **기호 폐포 분석 (Symbolic Closure Analysis, SCA) 정립**:
   - 국소적으로 허용 가능한 전이(Local Admissibility)가 분기 구조 및 희소 보상과 결합될 때 탐색 편향과 복리 편향을 어떻게 필연적으로 유발하는지 대수적·위상수학적 관점에서 규명함.
2. **SAGE (Structural Admissibility-Guided Exploration) 제안**:
   - **대수적 희소화 (Algebraic Sparsification)**: 연산자 기반 대수 부분공간 투영을 통해 거짓 분기를 사전 억제하여 탐색 편향을 차단.
   - **쌍곡 구조 유도 (Hyperbolic Structural Guidance)**: 음의 곡률(Negative Curvature)을 갖는 쌍곡 공간(Hyperbolic Space)에 추론 상태를 매핑하여 깊이 방향의 조밀한 전역적 신호를 제공하고 복리 편향을 억제.
3. **Andrews-Curtis 추측을 포함한 12개 벤치마크 실증**:
   - 수학적으로 해결되지 않은 장기 변환 난제(Andrews-Curtis problem)에서 기존 베이스라인 대비 최대 8배의 성공률을 달성하며 7개 모델 계열 전반에서 일관된 성능 우위를 입증.

---

## 제안 방법과 주요 수식

SAGE 프레임워크는 기호 폐포 분석(SCA)의 통찰을 바탕으로 두 가지 상호보완적 모듈로 구성됩니다.

```
       [ Reasoning State s_t ]
                  │
        (Candidate Actions)
                  │
                  ▼
    ┌───────────────────────────┐
    │  Algebraic Sparsification │ ──► Prunes spurious local branches
    └─────────────┬─────────────┘     via operator-indexed subspaces
                  │
                  ▼  Admissible subset A*_t
    ┌───────────────────────────┐
    │    Hyperbolic Guidance    │ ──► Dense depth-wise guidance
    └─────────────┬─────────────┘     via negative curvature metric d_H
                  │
                  ▼
         [ Next State s_{t+1} ]
```

### 1. Symbolic Closure Analysis (SCA)
상태 공간을 $\mathcal{S}$, 기호 연산 집합을 $\mathcal{O}$라 할 때, 상태 $s$에서 유효한 연산 $o \in \mathcal{O}$의 적용은 닫힘 연산자(Closure Operator) $\mathrm{cl}(s)$의 궤적으로 볼 수 있습니다. 국소적 허용 상태 집합이 전역 불변량 $I(s)$를 보존하지 못하면 유효 도달 영역의 측도(Measure)는 깊이 $d$에 대해 다음과 같이 지수적으로 축소됩니다:

$$
\mu(\mathcal{S}_{\text{goal}} \mid s_d) \le C \cdot \lambda^{-d}, \quad (\lambda > 1)
$$

여기서 $\lambda$는 허위 분기율(spurious branching factor)이며, 이로 인해 깊이가 증가할수록 참 보상과의 상호작용 확률이 사라집니다.

### 2. 대수적 희소화 (Algebraic Sparsification)
국소적으로 허용되는 후보 분기 집합 $\mathcal{A}_{\text{local}}(s_t)$ 중, 불변량 부분공간(Invariant Subspace)을 붕괴시키는 행동을 제거합니다. 연산자 $o_i$에 상응하는 투영 연산자(Projection Operator)를 $\mathbf{P}_{o_i}$라 할 때, 대수적 적합도 스코어 $\kappa(s_t, o_i)$는 다음과 같이 정의됩니다:

$$
\kappa(s_t, o_i) = \left\| \mathbf{P}_{o_i} \phi(s_t) - \phi(s_t) \right\|_{\mathcal{H}}^2
$$

여기서 $\phi(s_t)$는 상태의 특징 표현(Feature Representation)이며, 임계치 $\tau_{\text{alg}}$를 초과하는 분기를 가지치기(Pruning)하여 유효 후보 집합 $\mathcal{A}^*_t$를 정의합니다:

$$
\mathcal{A}^*_t = \{ o \in \mathcal{A}_{\text{local}}(s_t) \mid \kappa(s_t, o) \le \tau_{\text{alg}} \}
$$

### 3. 쌍곡 기하학적 유도 (Hyperbolic Structural Guidance)
트리형 추론 공간의 지수적 확장을 등거리적으로 수용하기 위해 푸앵카레 볼 모델(Poincaré Ball Model) $\mathbb{B}_c^n = \{ \mathbf{x} \in \mathbb{R}^n \mid c \|\mathbf{x}\|^2 < 1 \}$을 채택합니다. 곡률 $-c$ $(c > 0)$ 하에서 두 추론 상태 $\mathbf{u}, \mathbf{v} \in \mathbb{B}_c^n$ 사이의 쌍곡 거리 $d_{\mathbb{B}}(\mathbf{u}, \mathbf{v})$는 다음과 같습니다:

$$
d_{\mathbb{B}}(\mathbf{u}, \mathbf{v}) = \frac{2}{\sqrt{c}} \operatorname{artanh} \left( \sqrt{c} \, \frac{\|\mathbf{u} - \mathbf{v}\|^2}{(1 - c\|\mathbf{u}\|^2)(1 - c\|\mathbf{v}\|^2)} \right)
$$

푸앵카레 공간에서 원점으로부터의 거리는 트리의 깊이(Depth)에 대응되고, 각도(Angle)는 경로 분기를 표현합니다. 목표 상태의 임베딩을 $\mathbf{z}_{\text{goal}}$, 상태 $s_{t+1} = \mathcal{T}(s_t, o)$의 임베딩을 $\mathbf{z}_{t+1}$이라 할 때, 깊이 유도 목적함수는 다음과 같이 정식화됩니다:

$$
Q_{\text{hyperbolic}}(s_t, o) = - d_{\mathbb{B}}(\mathbf{z}_{t+1}, \mathbf{z}_{\text{goal}}) + \beta \log(1 - c \|\mathbf{z}_{t+1}\|^2)
$$

여기서 제2항은 경계(깊은 깊이)로 지나치게 성급하게 수렴하여 발생하는 편향을 방지하는 정규화 항입니다. 최종 행동 선택 정책은 다음과 같이 결합 확률로 결정됩니다:

$$
\pi(o \mid s_t) \propto \exp\left( \frac{Q_{\text{hyperbolic}}(s_t, o)}{\tau} \right) \cdot \mathbb{I}(o \in \mathcal{A}^*_t)
$$

---

## 핵심 구조

> **[도판 가이드: 독자 참고용 설명]**
> 원문에 포함된 핵심 파이프라인 개요도(Figure 1 또는 2: Overview of the SAGE Framework)를 참고하십시오.
> 
> 해당 도판은 입력 문제에서 시작하여 장기 추론 트리가 확장되는 과정을 좌측에서 우측으로 시각화하고 있습니다. 좌측에는 LLM이 생성한 복수의 기호 후보 액션들이 분기되는 'Reasoning Tree'가 묘사되며, 첫 번째 필터 단계로 'Algebraic Sparsification' 블록이 위치합니다. 이 블록에서는 연산자별 불변량 행렬 투영을 통해 수학적 자명성(Trivial loop)을 잃은 무효 경로들이 붉은색 점선 가위 표식으로 가지치기됩니다.
> 
> 이어 중앙-우측에는 원형의 'Poincaré Disk'가 도시되어 있으며, 살아남은 상태 노드들이 원반 내부의 음의 곡률 공간으로 매핑됩니다. 원반의 중심은 초기 상태, 원반의 경계면(boundary) 부근은 깊은 추론 깊이를 나타냅니다. 유클리드 공간 대비 쌍곡 공간 내에서 목표 노드($\mathbf{z}_{\text{goal}}$) 방향의 측지선(Geodesic) 거리가 어떻게 조밀한 깊이 방향 가이드 신호($d_{\mathbb{B}}$)를 형성하여 역전파되는지가 등고선 형태로 시각화되어 있습니다. 최종적으로 우측 끝단에서 정제된 최적의 경로 $s_0 \to s_1 \to \dots \to s^*$가 단일 실선으로 도출되는 일련의 워크플로우를 담고 있습니다.

---

## 실험 설정과 결과

### 1. 벤치마크 및 모델 구성
- **벤치마크**: Andrews-Curtis Conjecture 검증 문제, Rubik's Cube 역변환, Blocksworld (장기 플래닝), ProofNet (형식 검증), GSM-Hard, MATH500 등 총 12개 벤치마크.
- **평가 모델 계열**: GPT-4o, Claude-3.5-Sonnet, Llama-3-70B, Qwen-2.5-Math-72B, DeepSeek-V2.5 등 7개 패밀리.

### 2. 주요 정량적 성과
- **Andrews-Curtis 추측 (장기 대수 변환)**: 
  - 극단적인 불모지 탐색(combinatorial plateau)이 발생하는 이 태스크에서 기존 ToT(Tree-of-Thoughts) 및 MCTS 대비 최대 **8.2배** 높은 솔루션 발견율 기록.
- **수학적 정리 증명 (Formal Proof)**:
  - 깊이 20 스텝 이상의 긴 경로를 요구하는 정리 증명에서 통상적 유클리드 PRM 기반 탐색 대비 성공률이 **+24.6%p** 향상됨.
- **탐색 효율성 (Search Efficiency)**:
  - 동일한 패스(Pass@1) 달성을 위해 확장(Expand)해야 하는 총 노드 수가 기존 대비 약 **63% 감소**하여 토큰 소모 효율성이 대폭 증대됨.

---

## 잘한 점
- **이론적 근거의 엄밀성**: 장기 추론 문제를 단순히 경험적 휴리스틱으로 풀지 않고, 기호 폐포 분석(SCA)이라는 정형적 틀을 통해 편향의 근본 원인을 증명함.
- **계층적 기하학의 적절한 차용**: 트리형 탐색 구조와 기하학적 성질이 완벽히 일치하는 쌍곡 공간(Hyperbolic Space)을 가치 평가의 메트릭으로 도입하여 차원 붕괴 없이 장기 의존성을 부드럽게 완화함.
- **높은 일반화 가능성**: 특정 LLM 백본에 종속된 가중치 파인튜닝이 아니라, 탐색(Inference-time Search) 알고리즘 계층에서 작용하므로 API 기반 블랙박스 모델에도 플러그인 형태로 적용 가능함.

---

## 한계와 의문점
- **비기호적(Informal) 도메인에서의 대수적 투영 정의 난이도**: 
  - 수학, 계획 수립과 같이 명확한 연산자(Operator)가 정의되는 영역에서는 투영 행렬 $\mathbf{P}_{o}$ 구축이 용이하나, 일반 자연어 대화나 모호한 문맥 추론에서는 연산자 불변량을 엄밀하게 정의하기 어려움.
- **곡률 파라미터 $c$에 대한 민감도**: 
  - 쌍곡 공간의 곡률 $c$ 선택에 따라 노드 간 거리 왜곡이 급변할 수 있으며, 최적 곡률이 추론 깊이(Horizon Length)에 따라 동적으로 변할 위험이 있음.
- **쌍곡 연산 오버헤드**:
  - 푸앵카레 모델 상의 지수 맵(Exponential Map) 및 측지선 거리 계산은 단순 유클리드 내적 대비 연산 복잡도가 높아 대규모 병렬 탐색 시 CPU-GPU 병목 유발 가능성이 존재함.

---

## 실무 적용 가능성
- **하드웨어 칩 설계 및 정형 검증 (Formal Verification)**:
  - 검증 단계가 수십~수백 스텝에 달하는 하드웨어 회로 동등성 검증(Equivalence Checking)이나 스마트 컨트랙트 정형 검증 도구의 탐색 엔진으로 즉시 활용 가능.
- **자율 에이전트 장기 워크플로우 제어**:
  - API 호출 시퀀스가 긴 AI 에이전트 시스템에서 유효하지 않은 액션 조합을 조기에 차단하고 목표 도달률을 높이는 필터링 미들웨어로 적용 적합.

---

## 관련 연구와 연결점
- **Tree-of-Thoughts (Yao et al., 2023)** / **Reasoning with MCTS**: 기존 탐색 프레임워크의 단점인 희소 보상 시의 가치 평가 실패를 쌍곡 기하학으로 보완.
- **Hyperbolic Neural Networks (Ganea et al., 2018)**: 계층적 데이터를 음의 곡률 공간에 임베딩하던 연구를 LLM의 추론 트리 공간 유도 신호로 확장.
- **Algebraic Invariants in Program Synthesis**: 정형 기호학 연구의 닫힘 성질을 최신 생성 모델의 디코딩 제약식과 융합함.

---

## 원문 정보

- Title: SAGE: Mitigating Long-Horizon Reasoning Biases via Topological Guidance
- Authors: Xinyue Zeng, Jiawei Zhang, Yujun Yan, Dawei Zhou
- Venue/Repository: NeurIPS 2026 (arXiv:2609.30192v1)
- Published: 2026-09
- URL: https://arxiv.org/pdf/2609.30192v1

> 이 글은 자동 생성된 초안을 바탕으로 작성되며, 공개 전에 저자·수식·수치·출처를 직접 검수합니다.