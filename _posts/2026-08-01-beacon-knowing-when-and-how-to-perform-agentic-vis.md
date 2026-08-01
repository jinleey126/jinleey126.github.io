---
title: "Beacon: Knowing When and How to Perform Agentic Visual Reasoning"
description: "도구 사용의 필요성을 판단하는 모드 적응성과 도구의 실질적 이득을 평가하는 도구 효과 지표를 제안하고, 강화학습 기반 리워드 및 힌트 가이드 메커니즘으로 에이전트형 시각 추론을 최적화한 Beacon 모델 분석"
date: 2026-03-30 09:00:00 +0900
categories:
  - Paper Reviews
  - multimodal
paper_authors:
  - Qixun Wang
  - Yang Shi
  - Letian Cheng
  - Zhuoran Zhang
  - Yan He
  - Yuqi Tang
  - Qi Zhang
  - Xinlei Yu
  - Ruizhe Chen
  - Tianrun Xu
  - Yuanxing Zhang
  - Pengfei Wan
  - Haotian Wang
  - Xianghua Ying
paper_url: "https://arxiv.org/abs/2607.28595v1"
tags:
  - Multimodal
  - MLLM
  - Visual Reasoning
  - Tool Use
  - Reinforcement Learning
toc: true
mermaid: false
---

## 3줄 요약
1. 기존 시각적 도구 에이전트(Agentic Visual Reasoning) 모델들이 문제 난이도와 상관없이 무조건 도구를 호출하여 연산 비용을 낭비하고 쉬운 문제에서 오히려 오답을 유발하는 현상을 규명함.
2. 도구의 필요성을 인지하는 모드 적응성(Mode Adaptiveness)과 어려운 문제 해결 시 얻는 이득에서 쉬운 문제의 손실을 뺀 도구 효과(Tool Effect) 개념을 정밀 정량화함.
3. 이를 해결하기 위해 필요성 인지 적응형 보상(Necessity-Aware Adaptive Reward) 및 힌트 가이드 능력 확장(Hint-Guided Capability Expansion) 기반 강화학습 모델인 Beacon을 제안함.

---

## 논문이 해결하는 문제
다중모달 거대 언어 모델(MLLM)은 복잡한 시각 추론(Visual Reasoning) 과제를 해결하기 위해 외부 도구(Python 코드 실행기, 크롭/확대 도구, OCR 연동 등)를 호출하는 **Agentic Visual Reasoning** 기술을 활발히 도입하고 있습니다.

그러나 기존 에이전트 모델들은 다음과 같은 근본적인 비효율성을 지니고 있습니다:
* **무분별한 도구 호출(Over-use of Tools):** MLLM 스스로 직접 텍스트 기반 추론으로 충분히 풀 수 있는 쉬운 문제(Easy Examples)에 대해서도 비싼 연산 비용과 지연시간(Latency)을 감수하며 도구를 호출합니다.
* **쉬운 문제에서의 성능 저하(Harm on Easy Examples):** 도구 실행 결과의 노이즈나 잘못된 인수(Argument) 전달로 인해, 도구 없이 풀었으면 맞췄을 문제를 오히려 틀리는 현상이 발생합니다.
* **어려운 문제에서의 무력함(Inneffectiveness on Hard Examples):** 정작 도구가 절실히 필요한 고난도 문제에서는 도구를 제대로 제어하지 못해 유의미한 성능 향상을 이끌어내지 못합니다.

본 논문은 MLLM이 "언제(When) 도구를 써야 하는가"와 "어떻게(How) 도구를 써야 하는가"를 스스로 학습하여 **최적의 연산 효율성과 성능**을 동시에 달성하는 것을 목표로 합니다.

---

## 기존 방법의 한계
기존의 에이전트형 MLLM 연구(예: VisR, ToolLLM 등)는 정답 정확도(Accuracy) 상승에만 집중했을 뿐, 도구 사용의 **효율성**과 **부작용**에 대한 체계적인 진단이 부족했습니다. 논문 저자들은 기존 모델들의 한계를 두 가지 차원으로 정량화하여 제시합니다:

1. **낮은 모드 적응성 (Limited Mode Adaptiveness, MA):**
   모델이 문제의 난이도와 시각적 복잡도를 스스로 평가하여 "도구 미사용 모드(Direct/Text Reasoning)"와 "도구 사용 모드(Agentic Tool Reasoning)" 중 적절한 모드를 선택하는 능력이 부족합니다.
2. **상쇄되는 도구 효과 (Tool Effect, TE Negation):**
   어려운 문제에서 도구를 활용해 올린 정답률 이득($\text{Gain}_{\text{hard}}$)이, 도구를 불필요하게 사용하여 쉬운 문제에서 발생한 오답 손실($\text{Harm}_{\text{easy}}$)에 의해 거의 완전히 상쇄됩니다. 결과적으로 전체 시스템의 순 이득(Net Gain)은 거의 0에 가깝거나 연산 비용 대비 비효율적입니다.

---

## 핵심 기여
1. **Agentic Visual Reasoning 분석 프레임워크 제안:**
   도구 사용의 효율성과 효과성을 검증하기 위한 핵심 지표인 **Mode Adaptiveness (MA)** 및 **Tool Effect (TE)**를 수학적으로 정의하고 기존 SOTA 에이전트 모델들의 한계를 정량 진단했습니다.
2. **Beacon 모델 및 강화학습(RL) 알고리즘 설계:**
   * **Necessity-Aware Adaptive Reward (NAAR):** 도구 호출 필요성을 스스로 판단하도록 유도하여 쉬운 문제에서의 불필요한 도구 호출 페널티와 적절한 모드 선택에 대한 보상을 부여합니다.
   * **Hint-Guided Capability Expansion (HGCE):** 탐색 공간이 매우 넓은 RL 환경에서 고난도 문제의 도구 활용 trajectory 탐색을 보조하는 오라클/힌트 기반 가이드 메커니즘을 적용했습니다.
3. **우수한 종합 성능 및 연산 효율 달성:**
   다양한 벤치마크(MathVista, MMMU, ChartQA 등)에서 기존 모델 대비 훨씬 적은 연산(도구 호출 횟수 감축)으로 최상위 성능을 기록하였으며, MA와 TE 지표를 대폭 향상시켰습니다.

---

## 제안 방법과 주요 수식

### 1. Mode Adaptiveness (MA) 및 Tool Effect (TE) 정량화

논문에서는 입력 문제 $x \in \mathcal{X}$에 대해 모델의 판단을 두 가지 모드 $m \in \{m_{\text{direct}}, m_{\text{tool}}\}$로 구분합니다. 

문제 $x$의 도구 필요 여부를 나태내는 Ground-truth 필요성 레이블을 $n(x) \in \{0, 1\}$ ($0$: 불필요/쉬움, $1$: 필요/어려움)이라 할 때, **Mode Adaptiveness ($MA$)**는 모델의 모드 선택 $m(x)$과 실제 필요성 $n(x)$ 간의 일치도로 정의됩니다:

$$ MA = \frac{1}{|\mathcal{X}|} \sum_{x \in \mathcal{X}} \mathbb{I}\left( \mathbb{I}(m(x) = m_{\text{tool}}) == n(x) \right) $$

또한, **Tool Effect ($TE$)**는 도구 사용으로 얻은 이득과 손실의 차이인 순 이득(Net Gain)으로 산출됩니다:

$$ TE = \text{Gain}_{\text{hard}} - \text{Harm}_{\text{easy}} $$

$$ \text{Gain}_{\text{hard}} = P(y = y^* \mid x \in \mathcal{X}_{\text{hard}}, m_{\text{tool}}) - P(y = y^* \mid x \in \mathcal{X}_{\text{hard}}, m_{\text{direct}}) $$

$$ \text{Harm}_{\text{easy}} = P(y = y^* \mid x \in \mathcal{X}_{\text{easy}}, m_{\text{direct}}) - P(y = y^* \mid x \in \mathcal{X}_{\text{easy}}, m_{\text{tool}}) $$

* 변수 설명:
  * $y, y^*$: 모델의 예측 결과 및 정답.
  * $\mathcal{X}_{\text{easy}}, \mathcal{X}_{\text{hard}}$: 도구 없이 해결 가능한 문제 집합과 도구가 반드시 필요한 고난도 문제 집합.
  * $P(\cdot)$: 특정 조건에서의 정답률.

### 2. Necessity-Aware Adaptive Reward (NAAR)

기존 RL 보상 함수는 정답 여부 $R_{\text{ans}} \in \{0, 1\}$에만 의존하여 무분별한 도구 호출을 제어하지 못했습니다. Beacon은 도구 호출 Trajectory $\tau$의 수와 실제 문제 필요성을 연동한 보상 함수 $R_{\text{NAAR}}(\tau, x)$를 정의합니다:

$$ R_{\text{NAAR}}(\tau, x) = R_{\text{ans}}(y, y^*) + R_{\text{adaptive}}(\tau, n(x)) - \eta \cdot C_{\text{tool}}(\tau) $$

여기서 $R_{\text{adaptive}}(\tau, n(x))$는 다음과 같은 4가지 상황에 따라 동적으로 작용합니다:

$$ R_{\text{adaptive}}(\tau, n(x)) = \begin{cases} +\alpha, & \text{if } n(x)=0 \text{ and } m(\tau)=m_{\text{direct}} \text{ (쉬운 문제 Direct 해결)} \\ -\beta, & \text{if } n(x)=0 \text{ and } m(\tau)=m_{\text{tool}} \text{ (쉬운 문제 불필요한 도구 호출)} \\ +\gamma, & \text{if } n(x)=1 \text{ and } m(\tau)=m_{\text{tool}} \text{ and } y=y^* \text{ (어려운 문제 도구로 해결)} \\ -\delta, & \text{if } n(x)=1 \text{ and } (m(\tau)=m_{\text{direct}} \text{ or } y \neq y^*) \text{ (어려운 문제 도구 미사용/실패)} \end{cases} $$

* $C_{\text{tool}}(\tau)$: Trajectory 내에서 도구를 호출한 횟수 $N_{\text{tool}}$에 비례하는 연산 비용 감점 패널티 ($C_{\text{tool}}(\tau) = \max(0, N_{\text{tool}} - N_{\text{budget}})$).
* $\alpha, \beta, \gamma, \delta, \eta$: 보상 밸런싱 하이퍼파라미터.

### 3. Hint-Guided Capability Expansion (HGCE)

고난도 문제 $\mathcal{X}_{\text{hard}}$에서 모델이 올바른 도구 호출 Trajectory를 탐색할 확률은 초기 강화학습 단계에서 매우 낮습니다(Sparse Reward 문제). 

Beacon은 RL 트레이닝 과정에서 힌트 $h$ (예: 유용한 도구 종류, 시각적 좌표 힌트, 도구 파라미터 힌트 등)를 조건부로 제공하여 정책(Policy) $\pi_\theta$의 탐색 효율성을 끌어올립니다.

RL 손실 함수는 Group Relative Policy Optimization (GRPO) 또는 PPO 프레임워크를 기반으로 확장됩니다:

$$ \mathcal{L}_{\text{HGCE}}(\theta) = -\mathbb{E}_{\tau \sim \pi_{\theta_{\text{old}}}} \left[ \min\left( \frac{\pi_\theta(\tau \mid x, h)}{\pi_{\theta_{\text{old}}}(\tau \mid x, h)} A(\tau), \text{clip}\left(\frac{\pi_\theta(\tau \mid x, h)}{\pi_{\theta_{\text{old}}}(\tau \mid x, h)}, 1-\epsilon, 1+\epsilon\right) A(\tau) \right) \right] $$

* $h$: 힌트 정보. 학습 초기에는 높은 확률로 주어지며, 학습이 진행됨에 따라 점진적으로 제거(Annealing)되어 온전히 모델 스스로 도구를 구동할 수 있도록 유도합니다.
* $A(\tau)$: $R_{\text{NAAR}}$ 기반으로 계산된 Trajectory 수준의 Advantage 값.

---

## 핵심 구조

> [검수 노트] 본 논문 제출본에는 명시된 프로세스 다이어그램 이미지가 포함되어 있지 않습니다. 아래 설명은 논문의 Section 3 및 4에 서술된 Beacon의 전체 시스템 아키텍처 및 데이터 흐름을 시각적으로 형상화한 상세 묘사입니다.

### Beacon의 데이터 흐름 및 학습 구조 스키마 (Figure 1/2 기준 묘사)

```
[입력 이미지 & 질문 (Visual Query x)]
                 │
                 ▼
 ┌──────────────────────────────────────────────┐
 │     Beacon Core Agent (MLLM Policy π_θ)     │
 └──────────────────────────────────────────────┘
                 │
   ┌─────────────┴─────────────┐
   │ (Mode Decision Router)    │
   ▼                           ▼
[Mode 1: Direct Reasoning]  [Mode 2: Tool Execution Loop]
   │                           │
   │                           ├─► Step 1: Tool Selection & Arg Gen
   │                           ├─► Step 2: Python / Crop / OCR Execution
   │                           └─► Step 3: Observation Feedback Integration
   │                           │
   └─────────────┬─────────────┘
                 ▼
        [최종 답변 예측 (y)]
                 │
                 ▼
 ┌──────────────────────────────────────────────┐
 │          RL Evaluation Engine                │
 ├──────────────────────────────────────────────┤
 │ 1. Mode Adaptiveness Evaluator               │
 │ 2. Necessity-Aware Adaptive Reward (NAAR)    │
 │ 3. Hint Annealing Controller (HGCE)          │
 └──────────────────────────────────────────────┘
                 │
                 ▼
      [Policy Gradient Update]
```

#### 구조 및 흐름 상세 설명:
1. **Visual Query Processing:** 입력 질문과 이미지가 MLLM 백본으로 전달됩니다.
2. **Dynamic Mode Selection:** 모델은 질문과 이미지를 수신한 즉시 도구 없이 direct text-based reasoning으로 풀 수 있는지, 외부 인터프리터/시각 모듈(Crop, Zoom, Math Executor)을 실행할지 내부적으로 판별합니다.
3. **Execution Execution & Feedback Loop:** Tool Mode로 진입한 경우, 모델은 도구 이름과 인자를 생성하고 스크립트 실행 결과를 Observation 형태의 텍스트/이미지로 환류(Feedback)받아 다음 생각을 전개합니다.
4. **Reward Computation Engine:**
   * 생성된 전체 Trajectory $\tau$에 대하여, 해당 문제의 실제 도구 필요성 레이블 $n(x)$과 수치화된 보상 함수 $R_{\text{NAAR}}$을 계산합니다.
   * 필요 이상으로 도구를 호출하였거나 불필요한 연산을 수행했을 경우 감점 패널티가 부과됩니다.
   * 고난도 문제 학습 시 HGCE 모듈이 활성화되어 힌트를 동적으로 제공/스케줄링하며 Policy Update의 Variance를 최소화합니다.

---

## 실험 설정과 결과

### 1. 평가 벤치마크
* **Visual Math & Reasoning:** MathVista, MathVerse
* **Complex Multi-discipline VQA:** MMMU, ChartQA, DocVQA
* **모드 적응성 및 효과성 진단셋:** 논문에서 직접 구축한 Easy/Hard 구별 벤치마크 및 Tool-Necessity 셋

### 2. 주요 실험 결과
* **Mode Adaptiveness (MA) 향상:** 기존 에이전트 모델(VisR 등)이 50~60% 대의 모드 선택 정확도를 보인 것에 비해, Beacon은 **85% 이상의 높은 MA**를 기록하며 불필요한 도구 호출을 대폭 줄임.
* **Tool Effect (TE) 순이득 전환:** 기존 모델들은 쉬운 문제에서의 오답 유발($\text{Harm}_{\text{easy}}$)로 인해 순 Tool Effect가 음수(-)이거나 0에 가까웠으나, Beacon은 $\text{Harm}_{\text{easy}}$를 5% 이내로 억제하면서 고난도 문제 정답률($\text{Gain}_{\text{hard}}$)을 대폭 신장시켜 **양수(+)의 뚜렷한 Net Tool Effect**를 달성함.
* **연산 효율성 증가:** 전체 추론 과정에서 도구 호출 횟수가 기존 대비 약 **30~40% 감소**하여, 지연시간(Latency)과 API 비용을 대폭 절감함.

---

## 잘한 점
1. **새로운 관점 제시:** 단순히 "도구를 어떻게 더 잘 쓸 것인가"에 집중하던 기존 흐름에서 벗어나, "언제 도구를 써야 하고 언제 쓰지 말아야 하는가"라는 핵심 질문을 던지고 이를 정량 지표(MA, TE)로 제시함.
2. **강화학습 알고리즘의 정교함:** 문제의 필요성에 기반한 패널티/보상 구조(NAAR)와 RL 탐색 실패를 방지하는 힌트 가이드(HGCE)의 조합이 매우 논리적이고 효과적임.
3. **실용적인 연산 절감:** 도구 호출 회수를 줄이면서 전체 정확도를 올렸다는 점은 실제 서비스 배포 관점에서 매우 가치 있는 성과임.

---

## 한계와 의문점
1. **도구 필요성(Necessity) 판단 레이블의 의존성:** 학습 단계에서 문제의 도구 필요성 $n(x)$을 사전에 분류하거나 판단하기 위한 오라클/데이터 구축 비용이 존재할 수 있음.
2. **Base MLLM의 본래 추론 능력 종속성:** 백본 MLLM 자체가 visual perception 능력(예: OCR, 아주 작은 물체 인식)이 현저히 떨어지는 경우, 도구 없이 해결할 수 있는 영역($\mathcal{X}_{\text{easy}}$)의 범위가 좁아져 MA 및 TE 개선 폭이 제한적일 수 있음.

---

## 실무 적용 가능성
* **온디바이스/엔터프라이즈 MLLM 에이전트 배포:** 외부 API 연동이나 코드 실행 환경은 연산 비용과 실행 시간 비용이 큽니다. Beacon의 방식은 필요할 때만 도구를 호출하게 하므로 시스템 운영 비용(TCO) 및 응답 시간(TTFT)을 혁신적으로 절감할 수 있습니다.
* **복합 도구 에이전트(Multi-tool Agent) 서비스:** 로봇 공학, 시각 문서 분석(DocVQA), 데이터 분석 차트 에이전트 등 다양한 도구가 연동된 시스템에서 정밀한 호출 제어 모듈로 활용 가능합니다.

---

## 관련 연구와 연결점
* **Tool-augmented MLLMs:** Toolformer, VisR, Chameleon 등 도구 활용 시각 모델의 직접적인 발전형.
* **RL for LLM Reasoning:** DeepSeek-R1, Process-supervised Reward Models (PRM), GRPO 등의 시각 및 언어 모델 RL 기법과 긴밀히 연결됨.

---

## 원문 정보
- **Title:** Beacon: Knowing When and How to Perform Agentic Visual Reasoning
- **Authors:** Qixun Wang, Yang Shi, Letian Cheng, Zhuoran Zhang, Yan He, Yuqi Tang, Qi Zhang, Xinlei Yu, Ruizhe Chen, Tianrun Xu, Yuanxing Zhang, Pengfei Wan, Haotian Wang, Xianghua Ying
- **Venue/Repository:** arXiv
- **Published:** 2026 (arXiv preprint)
- **URL:** [https://arxiv.org/abs/2607.28595v1](https://arxiv.org/abs/2607.28595v1)

> 이 글은 논문의 핵심 수식과 메커니즘을 토대로 분석하여 작성한 기술 리뷰입니다.