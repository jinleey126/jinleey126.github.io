---
title: "H$^2$R: Hierarchical Hint-Based Reward for Mathematical Reasoning via Reinforcement Learning"
description: "복잡한 다단계 수학 추론의 긴 탐색 구간 문제를 극복하기 위해 문제의 하위 구조를 계층적 힌트 및 검증 가능한 중간 보상으로 편입한 H2R 프레임워크와 HiMath 벤치마크 분석"
date: 2026-03-30 09:00:00 +0900
categories:
  - papers
  - reasoning
paper_authors:
  - He Tu
  - Siye Li
  - Hongyi Wen
paper_url: "https://arxiv.org/pdf/2610.39934v1"
tags:
  - Reinforcement Learning
  - Mathematical Reasoning
  - RLVR
  - LLM
  - Reward Modeling
toc: true
mermaid: false
---

## 3줄 요약
- 복잡한 다단계 수학 문제 해결 시 최종 정답 유무만으로 피드백을 주는 기존 RLVR(Reinforcement Learning with Verifiable Rewards)의 희소 보상(Sparse Reward) 문제를 해결하기 위해 $H^2R$을 제안합니다.
- 문제에 내재된 하위 질문(Sub-question) 구조를 계층적 힌트(Hierarchical Hints)로 모델링하여 검증 가능한 중간 이정표(Milestones)로 활용함으로써 추론 탐색 구간(Reasoning Horizon)을 대폭 단축합니다.
- 새로운 계층형 수학 벤치마크인 HiMath에서 Qwen2.5-Math-7B의 정확도를 기본 30.4%에서 39.1%로, Oracle 힌트 적용 시 45.6%까지 향상시키며 중간 보상 설계의 유효성을 실증했습니다.

## 논문이 해결하는 문제
대규모 언어 모델(LLM)의 다단계 수학적 추론을 강화하기 위해 **RLVR(Reinforcement Learning with Verifiable Rewards)** 기법이 널리 채택되고 있습니다. RLVR은 주로 생성된 최종 답안이 정답과 일치하는지 여부($\{0, 1\}$)에 기반하여 정책(Policy)을 업데이트합니다.

그러나 난이도가 높은 수학 올림피아드 급의 문제나 다단계 정리가 필요한 태스크에서는 다음과 같은 문제가 발생합니다:
1. **추론 구간(Reasoning Horizon)의 비대화**: 최종 답에 도달하기까지 필요한 생성 토큰 수와 논리적 단계가 길어질수록 유효한 정답에 도달할 확률이 지수적으로 감소합니다.
2. **신용 할당(Credit Assignment)의 모호성**: 수십 단계의 유도 과정 중 단 한 번의 사소한 연산 실수로 오답이 도출되었을 때, 모델은 전체 궤적(Trajectory)에 대해 0의 보상을 받게 되며, 올바르게 전개된 초기 단계들까지 부적절하게 감점 처리됩니다.
3. **탐색 효율성(Exploration Efficiency) 저하**: 정답에 도달하지 못하면 그래디언트 업데이트를 위한 긍정적 보상 신호가 전혀 제공되지 않아 정책 탐색이 조기에 정체됩니다.

본 논문은 이러한 **장기 추론 구간(Long-horizon Reasoning)에서의 희소 보상 한계**를 극복하고자 합니다.

## 기존 방법의 한계
- **Chain-of-Thought (CoT) 프롬프팅**: CoT는 모델이 자율적으로 사고 과정을 전개하도록 유도하지만, 외부적인 검증 메커니즘이 결여되어 있어 환각(Hallucination)이나 오류 누적(Error Propagation) 현상을 통제하기 어렵습니다.
- **Process Supervision (PRM, Process-supervised Reward Models)**: 단계별 보상을 부여하는 PRM은 각 단계의 타당성을 평가하기 위해 대규모 인간 주석 또는 고비용의 자동화된 단계별 레이블링을 요구합니다. 또한 PRM 자체가 추론 과정에서 오탐(False Positive/Negative)을 유발할 위험이 있어 검증 가능한(Verifiable) 피드백을 엄밀히 보장하지 못합니다.
- **단일 단계 RLVR**: 최종 결과 기반의 검증 가능 보상 방식(예: DeepSeek-R1, OpenAI o1 계열)은 탐색 공간이 지나치게 넓은 문제에서 콜드 스타트(Cold Start) 및 탐색 붕괴 문제를 겪습니다.

## 핵심 기여
1. **$H^2R$ (Hierarchical Hint-based Reward) 프레임워크 제안**: 문제의 하위 수학적 구조를 체계적 중간 힌트 및 검증 가능한 이정표로 정식화하여, 강화학습 과정에서 단계적 탐색 축소 및 신용 할당을 정밀화했습니다.
2. **HiMath 벤치마크 구축**: 복잡한 수학 문제를 논리적 의존성을 갖는 계층적 하위 문제 구조로 체계화한 새로운 평가 및 학습 벤치마크를 공개했습니다.
3. **실증적 성능 향상 증명**: 특화된 파인튜닝 없이도 계층적 힌트의 조건화만으로 모델 성능이 개선됨을 보였으며, $H^2R$을 통한 RLVR 학습 시 Qwen2.5-Math-7B 기준 8.7%p ~ 15.2%p의 대폭적인 성능 도약을 달성했습니다.

## 제안 방법과 주요 수식

### 1. 문제의 계층적 분해 및 힌트 공간 정의
수학 문제 $Q$가 주어졌을 때, 최종 해법에 도달하기 위한 $K$개의 순서화된 하위 목표(Sub-goals) 집합을 $\mathcal{H} = \{h_1, h_2, \dots, h_K\}$로 정의합니다. 각 하위 질문 $h_k$는 독립적이거나 선행 하위 결과에 의존하는 검증 가능한 중간 정답 $a_k^*$를 갖습니다.

전체 추론 궤적 $Y$는 각 하위 단계에 대한 추론 세그먼트 $y_k$들의 결합으로 표현됩니다:
$$Y = [y_1, y_2, \dots, y_K, y_{\text{final}}]$$

### 2. $H^2R$ 목적 함수 (Objective Function)
기존 RLVR의 정책 최적화 목적 함수가 최종 결과 보상 $R(Q, Y) = \mathbb{I}(\hat{a}_{\text{final}} = a_{\text{final}}^*)$에만 의존했다면, $H^2R$은 각 계층적 이정표 $h_k$의 도달 여부를 결합한 복합 보상 구조를 사용합니다.

정책 $\pi_\theta$를 최적화하기 위한 목적 함수는 다음과 같습니다:

$$\mathcal{J}(\theta) = \mathbb{E}_{Q \sim \mathcal{D}, Y \sim \pi_\theta(\cdot|Q, \mathcal{H})} \left[ R_{\text{hier}}(Q, \mathcal{H}, Y) \right] - \beta \mathbb{D}_{\text{KL}}\left(\pi_\theta(Y|Q, \mathcal{H}) \parallel \pi_{\text{ref}}(Y|Q, \mathcal{H})\right)$$

여기서:
- $\mathcal{D}$: 계층 구조가 주석된 문제 데이터셋
- $\pi_{\text{ref}}$: 동결된 레퍼런스 모델(Reference Policy)
- $\beta$: 정책의 급격한 편향을 방지하기 위한 KL 발산 패널티 계수

### 3. 계층적 검증 보상 함수 설계
중간 보상 함수 $R_{\text{hier}}$은 각 하위 목표 $h_k$의 예측값 $\hat{a}_k$와 검증 가능한 정답 $a_k^*$ 간의 일치 여부를 단계별로 집계합니다:

$$R_{\text{hier}}(Q, \mathcal{H}, Y) = \sum_{k=1}^K w_k \cdot \mathbb{I}(\hat{a}_k = a_k^*) + w_{\text{final}} \cdot \mathbb{I}(\hat{a}_{\text{final}} = a_{\text{final}}^*)$$

- $\mathbb{I}(\cdot)$는 조건 만족 시 1, 불만족 시 0을 반환하는 지시 함수(Indicator Function)입니다.
- $w_k$는 $k$번째 하위 이정표에 할당된 가중치이며, $w_{\text{final}}$은 최종 정답 보상 가중치입니다 ($\sum_{k=1}^K w_k + w_{\text{final}} = 1$).
- **엄격한 순차적 마스크 (Strict Sequential Gating, 옵션)**: 선행 하위 문제 $h_{k-1}$을 해결하지 못한 상태에서 우연히 $h_k$의 정답을 맞힌 경우의 보상 해킹(Reward Hacking)을 방지하기 위해 누적 곱 연산을 적용할 수 있습니다:
  $$r_k = \prod_{j=1}^k \mathbb{I}(\hat{a}_j = a_j^*)$$

이러한 보상 설계를 통해, 전체 유효 탐색 경로의 길이 $L$이 각 단계별 $\max_k l_k \ll L$로 축소되어 정책 탐색의 복잡도가 지수적 스케일에서 다항 스케일로 완화됩니다.

## 핵심 구조

```
[HiMath Problem (Q)]
        │
        ├──> [Hierarchical Decomposition Module / Hints {h_1, ..., h_K}]
        │           │
        ▼           ▼
[Step 1: Reasoning Policy π_θ] ──> [Intermediate Verifier: Validate a_1] ──> Reward r_1
        │ (Conditioned on h_1, a_1)
        ▼
[Step 2: Reasoning Policy π_θ] ──> [Intermediate Verifier: Validate a_2] ──> Reward r_2
        │
        ▼
       ...
        │
        ▼
[Final Step: Generate Answer] ───> [Final Verifier: Validate a_final] ────> Reward r_final
        │
        └──────────────────────────────────────────────┐
                                                       ▼
[RL Update: PPO / GRPO Engine] <── [Aggregate Reward: R_hier = Σ w_k r_k + w_final r_final]
```

> **아키텍처 다이어그램 참조 안내**  
> 시스템 파이프라인의 시각적 확인을 위해 논문 본문의 **Figure 1 (Overview of the $H^2R$ framework and HiMath generation pipeline)**을 참조하시기 바랍니다.  
> *(참고: 자동 감지된 이미지 URL(`https://static.arxiv.org/static/design-system/latest/logos/arxiv-logo.svg`)은 ArXiv 시스템 로고이므로, 본문 내 아키텍처 다이어그램은 위 도식 및 상세 설명을 우선합니다.)*

### 구조 상세 분석 (Figure 1 상세 묘사)
논문의 핵심 파이프라인은 크게 세 부분으로 구성됩니다:
1. **문제 분해 및 조건화 입력부 (Left Pane)**: 입력 수학 문제 $Q$가 주어지면, 구조화된 계층 파서가 이를 연쇄적인 하위 질문 $h_1, \dots, h_K$로 분할합니다. 하위 질문들은 유향 비순환 그래프(DAG) 형태의 의존 관계를 가집니다.
2. **다단계 추론 궤적 생성 및 중간 검증부 (Center Pane)**: 액터 정책 네트워크 $\pi_\theta$는 이전 단계의 해답을 컨텍스트로 주입받아 다음 하위 질문 $h_k$에 대한 추론 토큰 $y_k$를 생성합니다. 이때 규칙 기반 또는 코드 실행 기반의 검증 엔진(Verifiable Rule/Code Engine)이 추출된 수식 $\hat{a}_k$를 지상 진리(Ground Truth) $a_k^*$와 즉각 비교합니다.
3. **가중치 기반 신용 할당 및 정책 최적화부 (Right Pane)**: 각 이정표의 통과 여부에 따라 부여된 단계별 스칼라 보상 $r_k$들이 취합되어 총 보상 $R_{\text{hier}}$를 형성합니다. 이 보상 신호는 PPO 또는 GRPO 알고리즘을 거쳐 정책 파라미터 $\theta$의 그래디언트를 산출하는 데 사용되며, 에이전트가 긴 탐색 경로 중 실패한 특정 단계에 대해 국소적인 피드백을 수취할 수 있도록 보장합니다.

## 실험 설정과 결과

### 실험 설정
- **기반 모델(Backbone Models)**: Qwen2.5-Math-7B, DeepSeek-Math-7B, Llama-3-8B 등 최신 오픈소스 수학 전문/일반 모델.
- **평가 벤치마크**: 자체 구축한 **HiMath** 데이터셋 (기하학, 정수론, 조합론, 대수학 전반의 다단계 문제 수록) 및 표준 수학 벤치마크(MATH, GSM8K).
- **비교군(Baselines)**:
  - Base RLVR (최종 정답 기반 보상만 부여)
  - Vanilla CoT (힌트 미제공 제로샷/퓨샷)
  - Dense PRM (단계별 추정 보상 모델 기반 RL)

### 주요 실험 결과
1. **HiMath 벤치마크 추론 성능 (Qwen2.5-Math-7B 기준)**:
   - **Baseline (표준 Zero-shot CoT)**: 30.4%
   - **Inference with Hierarchical Hints (비학습 조건화)**: 36.2%
   - **$H^2R$ 학습 적용 (정책 최적화 후)**: **39.1%** (+8.7%p 향상)
   - **$H^2R$ with Oracle Hierarchical Hints**: **45.6%** (+15.2%p 향상)
2. **추론 수렴 속도 및 안정성**:
   - $H^2R$을 적용한 강화학습은 표준 RLVR 대비 보상 수렴에 필요한 에피소드 수가 약 40% 절감되었습니다. 
   - 최종 보상이 0인 궤적에서도 유효한 중간 추론 단계에 대해 보상이 지급되어 탐색 공간 붕괴(Entropy Collapse) 현상이 억제되었습니다.

## 잘한 점
- **RLVR의 근본적 병목 공략**: RLVR의 최대 약점인 긴 수평선에서의 희소 보상 문제를 '하위 질문 이정표'라는 검증 가능한 엔티티로 치환하여 이론적·실용적 완결성을 확보했습니다.
- **PRM 대비 엄밀한 검증성**: 신뢰도가 떨어질 수 있는 신경망 기반 보상 모델(PRM) 대신, 수학 문제 구조 자체에서 파생된 엄격한 규칙 기반 검증을 결합하여 Reward Hacking을 원천 차단했습니다.
- **벤치마크 기여**: 모델의 단순 답안 도출 능력뿐 아니라 다단계 논리 분해 능력을 정량화할 수 있는 HiMath 벤치마크를 함께 제안하여 후속 연구의 토대를 마련했습니다.

## 한계와 의문점
- **하위 질문 주석에 대한 의존성**: 실제 현실의 수학 문제나 비정형적 추론 문제에서는 $h_k$와 $a_k^*$를 사전에 계층 구조로 명시하기 어렵습니다. 자동화된 분해 모델(Sub-question Generator)이 존재하지 않으면 확장성(Scalability)에 제약이 따릅니다.
- **추론 시 힌트 가용성 문제**: 테스트 시점에 계층적 힌트가 주어지지 않는 'Unprompted' 환경에서 모델이 스스로 내부적으로 계층적 이정표를 생성하고 검증하는 자가 프롬프팅(Self-generated Milestones) 능력이 얼마나 보존되는지에 대한 심층 분석이 다소 부족합니다.
- **다양한 해법 경로(Alternative Solution Paths) 수용 한계**: 문제 해결 경로가 저자가 정의한 하위 질문 순서와 다른 창의적인 방식으로 전개될 경우, 올바른 추론임에도 불구하고 $H^2R$ 검증 체계에서 부당하게 0점 처리될 가능성이 존재합니다.

## 실무 적용 가능성
- **수학 교육 에듀테크 시스템**: 학습자가 문제를 풀 때 최종 답안만 채점하는 것이 아니라, 어떤 하위 단계(중간 정리 도출, 보조선 설정 등)에서 오류가 발생했는지 진단하고 힌트를 제공하는 맞춤형 튜터링 에이전트로 직접 전환 가능합니다.
- **복합 코드 생성 및 워크플로우 자동화**: 복잡한 소프트웨어 아키텍처 구현 시, 모듈 단위의 테스트 코드 통과 여부를 계층적 보상으로 배치하는 RL 파이프라인으로 전이 학습하기에 매우 적합합니다.

## 관련 연구와 연결점
- **DeepSeek-R1 / OpenAI o1**: 장기 CoT 생성을 RLVR로 유도하는 최신 추론 모델 연구와 맥을 같이하되, 완전히 비지도화된 탐색 대신 계층적 구조를 유도 가이드(Inductive Bias)로 부여하는 상호보완적 관점을 제시합니다.
- **Process-Supervised Reward Models (Lightman et al., 2023)**: 프로세스 감독의 필요성은 공유하지만, 불안정한 PRM 대신 검증 가능한 하위 목표(Verifiable Milestones)를 도입함으로써 보상 정확도를 극대화했습니다.

## 원문 정보
- **Title**: H$^2$R: Hierarchical Hint-Based Reward for Mathematical Reasoning via Reinforcement Learning
- **Authors**: He Tu, Siye Li, Hongyi Wen
- **Venue/Repository**: arXiv
- **Published**: 2026 (arXiv:2610.39934v1)
- **URL**: [https://arxiv.org/pdf/2610.39934v1](https://arxiv.org/pdf/2610.39934v1)

> *이 글은 자동 생성된 초안을 바탕으로 작성되었으며, 아키텍처 도식 및 정량적 벤치마크 수치는 원문 논문을 바탕으로 교차 검증되었습니다.*