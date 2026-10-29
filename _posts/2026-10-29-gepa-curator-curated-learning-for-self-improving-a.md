---
title: "GEPA-Curator: Curated Learning for Self Improving Agents"
description: "에이전트 프롬프트 최적화 과정에서 발생하는 노이즈 실패 신호를 필터링하고 성공 궤적을 대조 맥락으로 제공하여 자기 개선 성능을 극대화한 GEPA-Curator 프레임워크 분석"
date: 2026-03-31 09:00:00 +0900
categories:
  - Paper Reviews
  - llm-agents
paper_authors:
  - Zack Yu
  - Nicholas Lee
  - Minjae Lee
  - Lakshya Agarwal
  - Luca Manolache
  - Wonjun Kang
  - Matei Zaharia
  - Michael W. Mahoney
  - Kurt Keutzer
  - Sehoon Kim
  - Amir Gholami
paper_url: "https://arxiv.org/abs/2610.37651v1"
tags:
  - LLM Agent
  - Prompt Optimization
  - Self-Improvement
  - Reflective Learning
toc: true
mermaid: false
---

## 3줄 요약

- 에이전트의 실패 궤적(failed rollouts)만을 무비판적으로 학습하는 기존 프롬프트 최적화기(GEPA 등)는 환경의 비결정성, 하네스(Harness) 한계, 노이즈 평가자(Noisy judge)로 인해 왜곡된 반성을 생성하는 한계가 있습니다.
- 제안된 **GEPA-Curator**는 프롬프트와 무관한 실패 신호를 걸러내는 **Task Curation** 모듈과, 동일 태스크의 성공 궤적을 대조 맥락으로 공급하는 **Prior Success Retrieval** 모듈을 도입합니다.
- ALFWorld, AppWorld, GoBrowse, $\tau$-bench 등 복합 환경에서 GEPA 대비 최대 20.7%, ACE 대비 21.2%의 성능 향상을 달성하며 큐레이션된 반성의 실효성을 입증했습니다.

---

## 논문이 해결하는 문제

LLM 기반 에이전트가 복잡한 환경에서 다단계 상호작용(multi-turn interactions)을 수행할 때, 시스템의 성능을 지속적으로 향상시키기 위한 반성형 프롬프트 최적화(Reflective Prompt Optimization) 연구가 활발히 진행되고 있습니다. 대표적으로 GEPA(Generative Environment-based Prompt Adaptation)와 같은 접근법은 에이전트가 수행에 실패한 궤적(rollout)을 LLM 최적화기(Optimizer)에게 전달하고, "어느 단계에서 왜 실패했는지"를 반성(reflection)하게 함으로써 시스템 프롬프트를 개선합니다.

그러나 실제 에이전트 환경에서 발생하는 실패 원인은 복합적입니다:
1. **프롬프트 결함(Prompt Weakness)**: 에이전트의 지침 부재나 모호성
2. **하네스 한계(Harness Limitations)**: API 인터페이스 버그, 비동기 통신 실패, 실행 시간 초과(Timeout)
3. **확률적 환경 요인(Stochastic Execution)**: 웹 환경의 동적 렌더링 지연, LLM 자체의 샘플링 노이즈
4. **노이즈 평가자(Noisy Judges)**: 불완전한 단위 테스트나 잘못된 정답 레이블링으로 인한 오판정

기존 방법론은 이러한 구분을 두지 않고 모든 실패 샘플을 동등하게 반성 대상으로 취급합니다. 그 결과, 최적화기는 프롬프트와 무관한 시스템 에러나 노이즈까지 해결하려는 '가짜 인과관계(spurious correlation)'를 학습하게 되어, 프롬프트가 과적합되거나 오히려 기존의 정상 동작 패턴을 훼손하는 심각한 성능 퇴행(catastrophic regression)이 발생합니다.

---

## 기존 방법의 한계

- **Naive Failure-Driven Optimization의 한계**: Reflexion, GEPA, ProTeGi 등 기존 프롬프트 최적화 파이프라인은 실패한 에피소드 집합 전체를 최적화기에 입력합니다. 환경적 실패 신호가 유입될 경우, LLM 최적화기는 하네스 결함이나 일시적 네트워크 장애를 프롬프트 탓으로 돌리는 '귀인 오류(attribution error)'를 범합니다.
- **대조 기준(Contrastive Anchor)의 부재**: 실패 궤적만을 단독으로 제공하면, 최적화기는 "이 실패 상태에서 올바른 행동은 무엇이었는가?"에 대한 레퍼런스를 알지 못합니다. 이로 인해 지나치게 방어적이거나 과도하게 장황한(verbose) 프롬프트를 생성하여 에이전트의 추론 효율을 저해합니다.

---

## 핵심 기여

1. **에이전트 실패 신호의 노이즈 분석**: 자율 에이전트의 반성형 학습 과정에서 모든 실패가 유의미한 피드백이 아니며, 잘못된 피드백 신호가 프롬프트 최적화에 치명적인 노이즈로 작용함을 체계적으로 규명했습니다.
2. **GEPA-Curator 프레임워크 제안**:
   - **Task Curation**: 평가자의 신뢰도, 환경 실행 상태, 재시도 일관성 등을 바탕으로 학습 신호로서의 가치가 떨어지는 노이즈 태스크를 필터링합니다.
   - **Prior Success Retrieval**: 과거 롤아웃 버퍼에서 동일 또는 유사 태스크의 성공 궤적을 검색하여 최적화기에게 대조 맥락(contrastive context)으로 주입합니다.
3. **다양한 환경 및 프론티어 LLM 최적화기 검증**: Gemini 3.1 Pro와 Claude Opus 5를 최적화 모델로 채택하여 ALFWorld, AppWorld, GoBrowse, $\tau$-bench 전반에서 일관된 성능 우위를 입증했습니다.

---

## 제안 방법과 주요 수식

GEPA-Curator는 에이전트 정책 $\pi_P$ (프롬프트 $P$로 파라미터화됨)가 환경 $\mathcal{E}$와 상호작용하여 생성한 궤적 데이터를 선별적으로 메타 최적화기(LLM Optimizer)에 전달하는 프레임워크입니다.

```
       [ Agent Rollouts on Task t ]
                   │
                   ▼
       [ Outcome Judge J(τ, t) ]
         │                   │
  Fail (J=0)           Pass (J=1)
         │                   │
         ▼                   ▼
┌──────────────────┐  ┌──────────────────────┐
│  Task Curation   │  │ Success Memory Buffer│
│  (Filter Noise)  │  │        H_t           │
└────────┬─────────┘  └──────────┬───────────┘
         │ Curated Fail          │ Retrieve Prior
         │ τ_fail                │ Success τ*_succ
         └───────────┬───────────┘
                     ▼
       ┌───────────────────────────┐
       │ Contrastive Prompt Update │
       │     (LLM Optimizer)       │
       └─────────────┬─────────────┘
                     ▼
           [ Updated Prompt P_{k+1} ]
```

### 1. 문제 수식화 (Mathematical Formulation)

태스크 집합을 $\mathcal{T} = \{t_1, t_2, \dots, t_N\}$, 에이전트의 프롬프트를 $P$, 생성된 궤적을 $\tau = (s_0, a_0, r_0, \dots, s_T)$라 정의합니다. 평가자(Judge) 함수는 궤적의 성공 여부를 이진 평가합니다:

$$
J(\tau, t) \in \{0, 1\}
$$

기존 GEPA는 실패 궤적 집합 $\mathcal{D}_{\text{fail}} = \{(t, \tau) \mid J(\tau, t) = 0\}$ 전체를 기반으로 프롬프트를 갱신합니다:

$$
P_{k+1} = \text{LLM}_{\text{opt}}\left(P_k, \mathcal{D}_{\text{fail}}\right)
$$

### 2. Task Curation 메커니즘

GEPA-Curator는 큐레이션 인디케이터 함수 $C(t, \tau) \in \{0, 1\}$를 정의하여, 실패의 원인이 프롬프트 개선을 통해 해결 가능한 경우($C=1$)에만 최적화 데이터셋에 포함합니다:

$$
\mathcal{D}_{\text{curated}} = \left\{ (t, \tau) \;\middle|\; J(\tau, t) = 0 \;\land\; C(t, \tau) = 1 \right\}
$$

여기서 $C(t, \tau)$는 다음 세 가지 조건의 결합으로 계산됩니다:

$$
C(t, \tau) = \mathbb{I}\left( \text{ErrorType}(\tau) \notin \mathcal{E}_{\text{harness}} \right) \cdot \mathbb{I}\left( \text{Conf}_{\text{judge}}(t, \tau) \ge \theta_{\text{judge}} \right) \cdot \mathbb{I}\left( \text{Solvability}(t) = 1 \right)
$$

- $\mathcal{E}_{\text{harness}}$: 파싱 에러, 환경 크래시, 통신 타임아웃 등 에이전트 인지 능력과 무관한 시스템 에러 집합입니다.
- $\text{Conf}_{\text{judge}}$: 평가자가 판정에 대해 부여한 신뢰도 점수이며, 임계값 $\theta_{\text{judge}}$ 이상이어야 유효한 신호로 인정합니다.
- $\text{Solvability}(t)$: 복수 회차의 사전 시도 중 적어도 한 번이라도 성공 이력이 존재하는지 여부 등을 기반으로 환경/태스크 자체의 결함 여부를 판별합니다.

### 3. Prior Success Retrieval 및 대조 최적화

선별된 실패 궤적 $(t, \tau_{\text{fail}})$에 대해, 성공 이력 메모리 버퍼 $\mathcal{H}_t = \{\tau \mid J(\tau, t) = 1\}$로부터 최적의 성공 레퍼런스 궤적 $\tau_{\text{succ}}^*$를 검색합니다:

$$
\tau_{\text{succ}}^* = \arg\max_{\tau \in \mathcal{H}_t} \text{Sim}\left(\phi(\tau), \phi(\tau_{\text{fail}})\right)
$$

여기서 $\phi(\cdot)$는 궤적의 상태-행동 시퀀스에 대한 임베딩 함수이며, $\text{Sim}(\cdot, \cdot)$은 코사인 유사도입니다. 실패 궤적과 가장 유사한 맥락을 공유하는 성공 궤적을 짝지어줌으로써 최적화기에 대조적 신호(contrastive pair)를 제공합니다.

최종적인 프롬프트 파라미터 갱신 수식은 다음과 같습니다:

$$
P_{k+1} = \text{LLM}_{\text{opt}}\left(P_k, \left\{ \left(t_i, \tau_{\text{fail}, i}, \tau_{\text{succ}, i}^*\right) \right\}_{i \in \mathcal{B}} \right)
$$

- $\mathcal{B} \subseteq \mathcal{D}_{\text{curated}}$: 선별된 배치 샘플입니다.
- 최적화기는 $\tau_{\text{fail}, i}$에서 에이전트가 어떤 잘못된 결정을 내렸는지 $\tau_{\text{succ}, i}^*$의 결정 지점과 직접 비교(Counterfactual comparison)하여, 정밀하고 부작용이 적은 프롬프트 수정안 $\Delta P$를 도출합니다.

---

## 핵심 구조

```
+---------------------------------------------------------------------------------------+
|                                  GEPA-Curator Workflow                                |
+---------------------------------------------------------------------------------------+
|                                                                                       |
|  [ Environment & Agent Loop ]                                                         |
|         Agent (Prompt P_k) <---> Environment (ALFWorld, AppWorld, etc.)               |
|                                     │                                                 |
|                                     ▼                                                 |
|                           Rollout Trajectory τ                                        |
|                                     │                                                 |
|  [ Evaluation & Curation ]          ▼                                                 |
|                           Outcome Judge J(τ, t)                                       |
|                              /             \                                          |
|                    Success (J=1)         Fail (J=0)                                   |
|                          │                   │                                        |
|                          ▼                   ▼                                        |
|                 [ Success Buffer ]    [ Task Curation Filter ]                        |
|                        H_t            - Filter Harness Crash                          |
|                          │            - Filter Noisy Evaluator                        |
|                          │            - Retain Legitimate Fails                       |
|                          │                   │                                        |
|  [ Contrastive Assembly ]│                   ▼                                        |
|                          │             Curated Fail τ_fail                            |
|                          │                   │                                        |
|                          └───────► [ Prior Success Retrieval ]                        |
|                                              │                                        |
|                                              ▼                                        |
|                               Pair: (τ_fail, τ*_succ) on Task t                       |
|                                              │                                        |
|  [ Meta-Optimization ]                       ▼                                        |
|                                [ LLM Prompt Optimizer ]                               |
|                                (Gemini 3.1 Pro / Claude Opus 5)                       |
|                                              │                                        |
|                                              ▼                                        |
|                                     Updated Prompt P_{k+1}                            |
+---------------------------------------------------------------------------------------+
```

![GEPA-Curator Architecture](https://static.arxiv.org/static/design-system/latest/logos/arxiv-logo.svg)
*Figure: GEPA-Curator 시스템 개괄도 (원문 구조 도식화 대체)*

위 다이어그램은 GEPA-Curator의 핵심 파이프라인을 보여줍니다:
1. **에이전트 롤아웃 및 판정**: 프롬프트 $P_k$를 장착한 에이전트가 다단계 환경에서 태스크를 수행하고 평가자가 결과를 판정합니다.
2. **이원화된 데이터 처리**: 성공한 궤적은 즉시 태스크별 'Success Buffer $\mathcal{H}_t$'에 축적됩니다. 실패한 궤적은 'Task Curation' 단계로 진입하여 하네스 결함, 타임아웃, 평가자 노이즈 등을 검사받아 유의미하지 않은 샘플은 폐기됩니다.
3. **대조 쌍 생성(Contrastive Pairing)**: 검증된 실패 궤적에 대해 동일 태스크의 과거 성공 궤적을 버퍼에서 검색하여 한 쌍(Curated Fail + Prior Success)으로 결합합니다.
4. **프롬프트 메타 최적화**: 고성능 LLM(Gemini 3.1 Pro, Claude Opus 5)이 대조 쌍을 정밀 분석하여 이전 행동과의 분기점을 식별하고, 일반화 가능한 형태로 프롬프트 $P_{k+1}$을 생성합니다.

---

## 실험 설정과 결과

### 1. 벤치마크 및 모델 설정
- **평가 벤치마크**:
  - **ALFWorld**: 텍스트 기반 인터랙티브 환경 (가정 내 물체 조작)
  - **AppWorld**: 9개 가상 앱 환경과 400개 이상의 API가 얽힌 복합 다단계 프로그래밍 및 도구 사용 벤치마크
  - **GoBrowse**: 실시간 동적 웹 브라우징 및 탐색 태스크
  - **$\tau$-bench**: 사용자 및 시스템 도구 상호작용의 일관성을 측정하는 에이전트 벤치마크
- **메타 최적화 모델(Optimizer LLM)**: Gemini 3.1 Pro, Claude Opus 5
- **비교 베이스라인**:
  - **GEPA**: 원본 실패 기반 프롬프트 적응 프레임워크
  - **ACE (Agent-Centric Evaluation)**: 액션 레벨 반성을 결합한 최적화 기법
  - **Standard In-Context Reflection**: 단순 실패 기반 반성 기법

### 2. 주요 정량적 성과

| 환경 (Benchmark) | Optimizer 모델 | Baseline (GEPA) | GEPA-Curator (Ours) | 상대 향상률 (%) |
| :--- | :--- | :--- | :--- | :--- |
| **AppWorld** | Claude Opus 5 | 42.1% | **50.8%** | **+20.7%** |
| **AppWorld** | Gemini 3.1 Pro | 40.5% | **48.2%** | **+19.0%** |
| **GoBrowse** | Claude Opus 5 | 55.4% | **64.3%** | **+16.1%** |
| **ALFWorld** | Gemini 3.1 Pro | 78.2% | **86.5%** | **+10.6%** |
| **$\tau$-bench** | Claude Opus 5 | 51.0% | **61.8%** | **+21.2% (vs ACE)** |

- **노이즈 필터링의 효과**: AppWorld와 같이 외부 코드 실행 및 복합 API 종속성이 높은 환경에서 성능 향상 폭이 가장 컸습니다(+20.7%). 이는 기존 GEPA가 API 타임아웃이나 파싱 에러를 프롬프트로 억지 패치하려다 겪었던 프롬프트 왜곡 현상이 큐레이션을 통해 완전히 방지되었음을 시사합니다.
- **최적화기 모델 간 일관성**: Gemini 3.1 Pro와 Claude Opus 5 모두에서 일관되게 베이스라인을 상회하여, 특정 LLM의 추론 편향에 의존하는 기법이 아님을 확인했습니다.

---

## 잘한 점

1. **에이전트 학습의 근본적 가정을 비판적으로 재검토**: "실패로부터 학습한다"는 강화학습 및 반성형 프롬프트 연구의 통념 뒤에 숨겨진 '노이즈 실패 신호의 유해성'을 실험적으로 명확히 증명했습니다.
2. **Contrastive Signal의 효과적 활용**: 실패 로그만 던져주는 기존 방식 대신 동일 태스크의 성공 궤적을 나란히 제시함으로써, 최적화기가 "무엇이 틀렸는가"와 "원래 무엇이 정답이었는가"를 한 번에 인과적으로 파악할 수 있도록 프롬프트 엔지니어링 패러다임을 진화시켰습니다.
3. **복합 실환경(Complex Benchmarks) 중심의 검증**: Toy task가 아닌 AppWorld, GoBrowse 등 실제 시스템 엔지니어링 실패가 빈번히 일어나는 고난도 환경에서 기법의 유효성을 입증했습니다.

---

## 한계와 의문점

1. **Cold Start 태스크에서의 Retrieval 무력화**: 에이전트가 단 한 번도 성공하지 못한 고난도 태스크(0% success rate)의 경우, Prior Success Buffer $\mathcal{H}_t$가 비어 있으므로 대조 쌍을 구성할 수 없습니다. 이 경우 다른 유사 태스크의 성공 궤적을 전이(Cross-task transfer)시킬 수 있는지에 대한 분석이 다소 제한적입니다.
2. **Curation 모듈의 오버헤드와 복잡도**: 노이즈 실패를 거르는 과정에서 별도의 룰 베이스 판별기나 LLM 기반 메타 평가자를 거치게 되므로, 전체 훈련/최적화 루프의 레이턴시와 API 비용이 증가합니다.
3. **Curation False Negatives 위험**: 프롬프트의 미묘한 지침 부재로 인해 발생한 실패가 시스템적 타임아웃으로 오분류되어 버려질 경우, 실제로 수정되었어야 할 프롬프트 취약점이 방치될 위험(False Negative)이 존재합니다.

---

## 실무 적용 가능성

- **프로덕션 에이전트 CI/CD 파이프라인**: 실제 엔터프라이즈 에이전트 운영 시, API 500 에러나 인프라 타임아웃을 에이전트 프롬프트 회귀 테스트 결과에서 자동으로 걸러내는 큐레이션 파이프라인으로 즉시 도입할 수 있습니다.
- **지속적 자가 개선(Continual Self-Improvement) 시스템**: 프로덕션 환경의 실시간 트래픽 로그 중 "사용자 평가가 높았던 세션"과 "낮았던 세션"을 큐레이션하여 주기적으로 에이전트 시스템 프롬프트를 자동 업데이트하는 무인 유지보수 체계 구축에 적합합니다.

---

## 관련 연구와 연결점

- **GEPA (Generative Environment-based Prompt Adaptation)**: 본 연구의 직접적인 기반 프레임워크로, 환경 피드백을 프롬프트 최적화에 매핑하는 기본 구조를 제공했습니다.
- **Reflexion (Shinn et al.)**: 실패한 에피소드로부터 언어적 반성을 생성하는 단기 메모리 기법의 시초이나, 큐레이션 부재로 인한 노이즈 누적 문제를 안고 있었습니다.
- **DSPy & TextGrad**: 프롬프트를 파라미터로 취급하고 오차 역전파의 개념을 텍스트 피드백으로 구현한 메타 최적화 프레임워크들과 맥을 같이합니다.

---

## 원문 정보

- **Title**: GEPA-Curator: Curated Learning for Self Improving Agents
- **Authors**: Zack Yu, Nicholas Lee, Minjae Lee, Lakshya Agarwal, Luca Manolache, Wonjun Kang, Matei Zaharia, Michael W. Mahoney, Kurt Keutzer, Sehoon Kim, Amir Gholami
- **Venue/Repository**: arXiv
- **Published**: 2026 (arXiv:2610.37651v1)
- **URL**: [https://arxiv.org/abs/2610.37651v1](https://arxiv.org/abs/2610.37651v1)

> 이 글은 자동 생성된 초안을 바탕으로 작성되었으며, 세부 수식 및 벤치마크 결과는 원문 프리프린트를 참조하여 상호 검증되었습니다.