---
title: "Bayesian Belief Layer for Controllable Opinion Dynamics in LLM Agents"
description: "LLM 에이전트의 발화 생성과 내부 신념 갱신을 분리하여 파라미터 기반으로 의견 역학을 제어하고 감사 가능하게 만드는 베이지안 신념 계층 제안"
date: 2024-09-24 09:00:00 +0900
categories:
  - papers
  - agent-simulation
paper_authors:
  - Hafsa Akbar
  - Daniel Platnick
  - Marjan Alirezaie
  - Hossein Rahnama
paper_url: "https://arxiv.org/pdf/2609.21997v1"
tags:
  - LLM Agents
  - Opinion Dynamics
  - Bayesian Updating
  - Social Simulation
  - Agentic Systems
toc: true
mermaid: false
---

## 3줄 요약

1. 기존 LLM 소셜 시뮬레이션은 에이전트의 설득 수용도(persuasion susceptibility)를 명시적으로 제어할 수 없고, 모델의 내재된 사전 편향(prior bias)에 크게 의존함.
2. 에이전트의 내부 신념($p \in [0, 1]$)과 언어 표출(utterance generation)을 엄격히 분리하고, 발언 청취 시 1회의 베이지안 사후분포 갱신을 수행하는 **Bayesian Chronicle Agents(BCA)** 구조를 제안함.
3. Friedkin–Johnsen(FJ) 역학의 고집도(stubbornness) 파라미터 $\kappa$를 제어 변수로 도입하여 합의, 지속적 불일치, 헌신적 소수자 영향 등 정형화된 여론 분포를 유도하고, FJ 닫힌 해(closed-form fixed point)와 $R^2 = 0.93 \sim 0.99$의 높은 일치도를 달성함.

---

## 논문이 해결하는 문제

대규모 언어 모델(LLM)을 활용한 다중 에이전트 사회 시뮬레이션(Social Simulation)은 현실적인 인간 상호작용과 여론 형성 과정을 모델링하는 도구로 널리 연구되고 있습니다. 그러나 기존 프롬프트 기반 에이전트는 다음과 같은 근본적인 결함을 안고 있습니다.

- **비제어성(Uncontrollability)**: 특정 에이전트가 타인의 의견에 얼마나 열려 있는지(openness) 혹은 얼마나 완고한지(stubbornness)를 프롬프트 지시문("너는 매우 고집스러운 사람이다")만으로 정량화하거나 검증할 수 없습니다.
- **불투명성 및 감사 불가능성(Inauditability)**: 에이전트의 의견 변화가 모델 내부 트랜스포머의 어텐션 및 컨텍스트 윈도우 내에서 암묵적으로 발생하므로, 특정 결론이 에이전트 간의 정당한 논리 교환에 의한 것인지, 혹은 사전학습 가중치에 내재된 잠재적 편향(pretrained bias)의 발현인지 추적하기 어렵습니다.
- **거시 역학과의 괴리**: 고전적인 사회물리학 및 네트워크 과학 기반의 여론 역학 모델(예: DeGroot 모델, Friedkin–Johnsen 모델)이 제시하는 수학적 평형 상태와 LLM 기반 텍스트 상호작용 사이의 연결 고리가 결여되어 있었습니다.

---

## 기존 방법의 한계

1. **End-to-End 프롬프트 의존성**:
   기존 시뮬레이션은 에이전트의 이전 대화 내역 전체를 컨텍스트에 누적하여 다음 발화를 생성하도록 유도합니다. 이 방식에서는 대화가 길어질수록 컨텍스트 내 위치 편향(recency bias)이나 생성 다양성 붕괴가 발생하며, 에이전트가 실제로 어떠한 신념 상태를 보유하고 있는지 직접 관측할 수 없습니다.
2. **사전 확률(Priors)의 잠식**:
   LLM은 특정 사회적 이슈(정치, 윤리, 정책 등)에 대해 특정 방향으로 편향된 텍스트 분포를 학습 데이터로부터 물려받습니다. 설득 실험을 수행할 때 이러한 내재적 사전 분포가 에이전트의 입장 전이를 지배하여, 순수하게 역학적 관계에 따른 시뮬레이션 결과를 왜곡합니다.
3. **정량적 민감도 조절 불가**:
   에이전트별로 '설득 저항성'을 0부터 1까지의 연속형 스칼라 값으로 조절할 수 있는 수학적 메커니즘이 존재하지 않아, 통제 변인 기반의 민감도 분석(sensitivity analysis)이 불가능했습니다.

---

## 핵심 기여

1. **내부 신념 계층(Bayesian Chronicle Agents, BCA)의 도입**:
   에이전트가 "무엇을 믿는지(belief state)"와 "어떻게 말하는지(speech generation)"를 분리하는 경량 베이지안 계층을 설계했습니다. 신념은 확률값으로 유지되며, 발화를 들을 때마다 명시적인 단일 베이지안 스텝을 통해 갱신됩니다.
2. **수학적 고집도 파라미터 $\kappa$ 도입 및 FJ 역학 연계**:
   Friedkin–Johnsen(FJ) 여론 역학의 핵심 파라미터를 차용하여 사전 분포의 가중치를 결정하는 단일 파라미터 $\kappa$(stubbornness)를 부여했습니다. 이를 통해 합의(Consensus), 지속적 불일치(Persistent Disagreement), 헌신적 소수자 영향(Committed-Minority Influence)의 세 가지 표준 역학 레짐(regime)을 결정론적으로 재현했습니다.
3. **이론적 닫힌 해와의 수치적 일치 검증**:
   지속적 불일치 조건에서 BCA 시뮬레이션의 최종 신념 상태가 FJ 모델의 닫힌 해(closed-form analytical fixed point)와 $R^2 = 0.93 \sim 0.99$의 극도로 높은 상관계수로 수렴함을 수학적·실험적으로 입증했습니다.
4. **언어 라운드트립(Language Round-trip) 하 파라미터 복원성 및 편향 감사**:
   자연어로 표현된 텍스트 발화를 거친 뒤에도 원래 주입된 고집도 $\kappa$의 순위 관계가 4개 LLM 전반에서 100% 복원(perfect rank-order recovery)됨을 보였으며, End-to-End 시뮬레이션에서는 드러나지 않던 각 LLM 고유의 내재적 입장 편향(stance bias)을 정량적으로 분리·적출했습니다.

---

## 제안 방법과 주요 수식

BCA는 에이전트 $i$의 신념 상태(Belief State) $p_i^{(t)} \in [0, 1]$를 명시적 잠재 변수로 정의합니다. 여기서 $p_i$는 특정 명제(Proposition)에 대한 지지 확률을 의미합니다.

### 1. Friedkin–Johnsen(FJ) 역학 기반 동기 부여

고전적인 FJ 여론 역학 모델에서 에이전트 집합의 의견 벡터 $x^{(t)} \in \mathbb{R}^n$의 갱신 규칙은 다음과 같습니다.

$$x^{(t+1)} = \Lambda W x^{(t)} + (I - \Lambda) x^{(0)}$$

여기서:
- $W \in \mathbb{R}^{n \times n}$는 에이전트 간의 상호작용 가중치 행렬(확률 보존 행렬, $\sum_j W_{ij} = 1$)입니다.
- $\Lambda = \text{diag}(1 - \kappa_1, \dots, 1 - \kappa_n)$는 감수성(susceptibility) 행렬입니다.
- $\kappa_i \in [0, 1]$는 에이전트 $i$의 고집도(stubbornness / anchoring to initial stance)를 나타냅니다.
- $x^{(0)}$는 각 에이전트의 초기 입장 벡터입니다.

만약 $I - \Lambda W$가 역행렬을 가지면, 시스템은 다음과 같은 유일한 정적 상태(fixed point)로 수렴합니다.

$$x^* = (I - \Lambda W)^{-1} (I - \Lambda) x^{(0)}$$

### 2. 베이지안 신념 계층 (Bayesian Belief Layer)의 수식화

BCA는 연속형 텍스트 토큰 상에서 역전파를 수행하는 대신, 켤레 사전분포(Conjugate Prior) 형태의 베타-이항(Beta-Binomial) 또는 가우스 관측 갱신을 이산 시간 스텝마다 적용합니다. 

에이전트 $i$의 초기 신념 $p_i^{(0)}$와 사전 분포 강도(effective prior sample size)를 고집도 $\kappa_i$와 스케일 인자 $N_0$의 곱으로 정의합니다. 즉, 사전 가중치(Prior weight) $M_i = \frac{\kappa_i}{1 - \kappa_i + \epsilon}$를 설정합니다.

시간 $t$에서 상대 에이전트 $j$의 발화 $u_j^{(t)}$를 청취했을 때, BCA의 신념 파서(Stance Parser)는 발화에서 전달되는 관측된 입장 신호(likelihood signal) $y_{j \to i}^{(t)} \in [0, 1]$를 추출합니다. 이후 단일 베이지안 갱신 단계(single Bayesian step)를 수행합니다.

$$p_i^{(t+1)} = \frac{\kappa_i p_i^{(0)} + (1 - \kappa_i) \sum_{j \in \mathcal{N}_i} W_{ij} y_{j \to i}^{(t)}}{\kappa_i + (1 - \kappa_i) \sum_{j \in \mathcal{N}_i} W_{ij}}$$

네트워크가 완전 연결망(fully connected)이고 발화자가 균등 선택된다면, 발화 청취에 따른 신념 갱신은 다음의 볼록 결합(convex combination)으로 단순화됩니다.

$$p_i^{(t+1)} = (1 - \alpha_i) p_i^{(t)} + \alpha_i y_{j \to i}^{(t)}$$

여기서 학습률(effective learning rate) $\alpha_i$는 고집도 $\kappa_i$의 단조 감소 함수로 정의됩니다.

$$\alpha_i = \frac{1}{\kappa_i \cdot \tau + 1}, \quad \tau > 0$$

$\kappa_i \to 1$일 때 $\alpha_i \to 0$이 되어 에이전트는 타인의 발화에 완전히 무반응(stubborn)하며, $\kappa_i \to 0$일 때 타인의 발화 신호에 최대치로 반응(fully susceptible)합니다.

### 3. 신념-언어 인터페이스 (Belief-to-Speech & Speech-to-Belief)

1. **Belief-to-Speech (생성)**:
   에이전트 $i$가 발화할 차례가 되면, 내부 신념 $p_i^{(t)}$를 프롬프트의 지시 제약 조건(예: "당신의 현재 명제 찬성 확률은 $p_i^{(t)}$입니다. 이 입장을 반영하여 자연스럽게 발언하십시오")으로 주입하여 텍스트 $u_i^{(t)}$를 생성합니다.
2. **Speech-to-Belief (관측 추출)**:
   청취 에이전트는 수신된 텍스트 $u_j^{(t)}$를 구조화된 파서를 통해 스칼라 우도 신호 $y_{j \to i}^{(t)} \in [0, 1]$로 투영합니다.

이로써 에이전트는 컨텍스트에 텍스트 전체를 무비판적으로 누적하지 않고, 압축된 통계량인 신념 $p_i$만을 상태(state)로 유지합니다.

---

## 핵심 구조

```
[Figure 1 Placeholder: Conceptual Diagram of Bayesian Chronicle Agents (BCA)]
* 논문 원문의 아키텍처 다이어그램(Figure 1: Overview of Bayesian Chronicle Agents framework)을 참조하십시오.
```

> **아키텍처 구조 상세 설명 (Figure 1 참조 가이드)**:
> 
> 해당 도표는 두 에이전트 간의 텍스트 교환 및 내부 상태 갱신 루프를 도식화한 것입니다.
> 1. **State Isolation**: 상단에는 각 에이전트의 내부 저장소(Agent Chronicle State)가 위치하며, 여기에는 스칼라 신념 값 $p_i^{(t)}$와 고집도 하이퍼파라미터 $\kappa_i$, 그리고 초기 기준점 $p_i^{(0)}$가 명시적으로 분리되어 저장됩니다.
> 2. **Speech Generation Path**: 에이전트 $A$의 내부 신념 $p_A^{(t)}$는 LLM Generator로 전달됩니다. Generator는 시스템 프롬프트 및 페르소나 설정과 함께 신념 값을 컨디셔닝 팩터로 입력받아 외부 발화(Utterance $u_A$)를 합성합니다.
> 3. **Communication Channel**: 생성된 발화 텍스트는 시뮬레이션 환경의 통신 채널을 거쳐 수신 에이전트 $B$의 인풋으로 인가됩니다.
> 4. **Bayesian Belief Update Path**: 수신 에이전트 $B$는 텍스트를 바로 LLM의 컨텍스트 윈도우에 밀어넣지 않고, 경량 파서 모듈(Likelihood Extractor)을 거치게 합니다. 추출된 입장 우도 $y$는 $B$의 기존 신념 $p_B^{(t)}$ 및 고립된 파라미터 $\kappa_B$와 결합하여 수식 기반의 베이지안 사후분포 갱신 엔진(Bayesian Update Step)으로 들어갑니다.
> 5. **Closed Loop**: 갱신된 새로운 신념 $p_B^{(t+1)}$가 상태 레지스터에 기록되고, 다음 턴에서 $B$가 발화할 때 이 새로운 $p_B^{(t+1)}$가 발화 생성 모듈로 공급되는 완전한 분리형 피드백 루프를 구성합니다.

---

## 실험 설정과 결과

### 1. 실험 환경 및 모델

- **대상 모델**: LLaMA-3-8B-Instruct, LLaMA-3-70B-Instruct, Mistral-7B-Instruct, GPT-4o-mini 등 4개 주요 LLM.
- **네트워크 구조**: 완전 연결 네트워크(Fully connected graph) 및 이중 군집 네트워크(Two-community graph).
- **시뮬레이션 토픽**: 원자력 발전 찬반, 보편적 기본소득(UBI), AI 규제 강도 등 실제 찬반 대립이 팽배한 사회적 논제.

### 2. 세 가지 정형 레짐(Canonical Regimes) 유도

| 레짐 (Regime) | 파라미터 조건 ($\kappa$) | 시뮬레이션 관측 결과 | FJ 이론값 일치도 ($R^2$) |
| :--- | :--- | :--- | :--- |
| **Consensus (합의)** | 모든 노드 $\kappa_i \to 0$ (극단적 유연성) | 집단 전체가 단일 중심 신념으로 완전 수렴 | $0.98$ 이상 |
| **Persistent Disagreement** | 노드별 $0 < \kappa_i < 1$ 분포 | 초기 성향에 고착되어 다극화(polarization) 유지 | **$R^2 = 0.93 \sim 0.99$** |
| **Committed Minority** | 소수 집단 $\kappa = 1.0$, 다수 집단 $\kappa \approx 0.1$ | 완고한 소수자가 전체 군집의 의견을 견인 | 정성적·정량적 역학 완벽 재현 |

### 3. 파라미터 복원성 (Parameter Recovery)

- 에이전트가 언어로 발화하고 이를 다시 타인이 청취하는 "Language Round-trip"을 거친 데이터에서, 사후적으로 에이전트들의 $\kappa$ 값을 추정한 결과, 테스트된 모든 모델(4종)에서 주입된 $\kappa$ 순위와 추정된 $\kappa$ 순위 간 스피어만 상관계수(Spearman's $\rho$)가 $1.0$을 기록했습니다.
- 즉, 언어적 표현의 모호성에도 불구하고 수학적으로 주입된 고집도 계층이 훼손되지 않고 보존됨을 확인했습니다.

### 4. 모델 내재적 편향(Inherent Stance Bias) 적출

- End-to-End 프롬프트 시뮬레이션에서는 에이전트들이 왜 특정 결론에 도달했는지 규명할 수 없었으나, BCA 계층을 통해 각 LLM이 발화를 생성할 때 신념 $p$에 체계적인 편향 오프셋 $\Delta(p) = \mathbb{E}[y] - p$을 가하고 있음을 확인했습니다.
- 예컨대 특정 오픈소스 모델은 동일한 $p=0.5$ 입력에 대해서도 텍스트 발화 시 평균 $0.62$ 수준의 친화적 스탠스로 치우쳐 발언하는 경향을 계측할 수 있었습니다.

---

## 잘한 점

1. **소프트웨어 공학 및 수학적 추상화의 분리**:
   LLM을 인지 상태를 통째로 모사하는 블랙박스로 취급하던 관행에서 탈피하여, '언어 표현 엔진'과 '수치적 신념 레지스터'로 역할을 명확히 분리함으로써 시뮬레이션의 해석 가능성을 극대화했습니다.
2. **사회물리학 이론과의 실질적 융합**:
   단순히 휴리스틱한 프롬프트 엔지니어링에 그치지 않고, 수십 년간 검증된 Friedkin–Johnsen 고전 역학의 수렴 방정식과 LLM 시뮬레이션을 수학적으로 연결하여 $R^2 \ge 0.93$이라는 매우 강력한 실증적 증거를 제시했습니다.
3. **블랙박스 편향 감사 프레임워크 제공**:
   사전학습된 LLM이 특정 토픽에 대해 갖는 내재적 편향을 역추적할 수 있는 진단 도구로서의 실용적 가치가 매우 높습니다.

---

## 한계와 의문점

1. **명제의 다차원성 제약**:
   현재 수식은 단일 쟁점에 대한 1차원 스칼라 확률 $p \in [0, 1]$에 국한되어 있습니다. 현실의 사회적 담론은 복합 명제 간의 논리적 얽힘(hyper-dimensional belief space)이 존재하는데, 이를 단일 베이지안 스텝으로 투영할 때 정보 손실이 발생할 수 있습니다.
2. **발화-우도 파서의 신뢰도 의존성**:
   자연어 텍스트에서 스칼라 우도 신호 $y$를 추출하는 파서(Parser) 모듈 자체의 성능에 시뮬레이션의 수렴성이 좌우될 위험이 있습니다. 파서가 복잡한 반어법이나 수사학적 비유를 오독할 경우 사후분포 갱신에 노이즈가 누적될 수 있습니다.
3. **토론의 논리적 타당성(Quality of Argument) 배제**:
   현재의 베이지안 갱신 수식에서 발화의 설득력은 우도 $y$로만 축약되며, 논증 구조의 엄밀성이나 사실성(Factuality)에 따라 가중치를 동적으로 부여하는 메커니즘은 고려되지 않았습니다.

---

## 실무 적용 가능성

- **정책 영향 평가 및 마케팅 여론 시뮬레이션**:
  신제품 출시나 공공 정책 도입 전, 타깃 집단의 수용도(openness) 파라미터 $\kappa$를 세그먼트별로 다르게 세팅하여 현실적인 여론 분극화 시나리오를 고정밀도로 예측할 수 있습니다.
- **AI 안전성 및 모델 레드팀(Red Teaming)**:
  다양한 모델들의 Stance Bias를 정량적으로 벤치마킹하는 감사 도구로 배포하여, 특정 LLM이 설득 과정에서 사용자 여론을 편향되게 왜곡할 위험성을 사전 검증할 수 있습니다.

---

## 관련 연구와 연결점

- **DeGroot (1974) & Friedkin–Johnsen (1990)**:
  본 논문의 이론적 토대를 형성하는 고전적 사회적 의견 형성 모델.
- **Generative Agents (Park et al., 2023)**:
  컨텍스트 기반 기억 검색 및 자연어 반추를 통해 사회적 상호작용을 구현했으나, 수치적 신념 상태가 없어 제어 불가능했던 기존 패러다임.
- **Auditing LLM Biases in Multi-agent Debates (2023~2024)**:
  LLM 간 토론 시 발생하는 다수결 쏠림 현상(sycophancy)이나 합의 강제 문제를 수학적 사전 확률 개념으로 해결하려는 최근 연구 흐름과 밀접하게 맞닿아 있습니다.

---

## 원문 정보

- **Title**: Bayesian Belief Layer for Controllable Opinion Dynamics in LLM Agents
- **Authors**: Hafsa Akbar, Daniel Platnick, Marjan Alirezaie, Hossein Rahnama
- **Venue/Repository**: The 2nd Workshop for Research on Agent Language Models (REALM) at EMNLP 2026 / arXiv:2609.21997v1
- **Published**: 2024-09 (arXiv preprint)
- **URL**: [https://arxiv.org/pdf/2609.21997v1](https://arxiv.org/pdf/2609.21997v1)

> *이 글은 자동 생성된 초안을 바탕으로 작성되며, 공개 전에 저자·수식·수치·출처를 직접 검수합니다.*