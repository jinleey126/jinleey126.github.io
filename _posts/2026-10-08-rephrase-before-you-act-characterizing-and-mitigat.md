```markdown
---
title: "Rephrase Before You Act: Characterizing and Mitigating Language Sensitivity in Vision-Language-Action Models"
description: "VLA 모델의 극심한 언어 표현 민감성을 체계적으로 규명하고, 정책 재학습 없이 소수의 재표현 규칙을 LLM으로 증류하여 추론 전 입력을 교정하는 프레임워크를 제안한 논문"
date: 2026-03-30 09:00:00 +0900
categories:
  - Paper Reviews
  - robotics
paper_authors:
  - Mikey Watts
  - Yuchen Cui
paper_url: "https://arxiv.org/abs/2610.10526"
tags:
  - Robotics
  - VLA
  - Prompt Engineering
  - Robustness
toc: true
mermaid: false
---

## 3줄 요약
- Vision-Language-Action(VLA) 모델($\pi_0$, $\pi_{0.5}$)은 기반이 되는 VLM의 언어 강건성을 온전히 상속하지 못하며, 단 한 단어의 동의어 치환만으로도 성공률이 수십 %p 급락하는 심각한 언어 민감도(Language Sensitivity)를 보인다.
- 이러한 취약점은 임의의 노이즈가 아닌 체계적인 편향(Systematic Bias)을 따르며, 최적의 표현(Oracle Phrase)을 선택하는 것만으로도 In-Distribution(ID)과 Out-of-Distribution(OOD) 태스크 간 성능 격차(21%p)가 거의 해소됨을 증명했다.
- 파인튜닝 데이터셋의 소수 태스크에서 표현 변형을 평가한 뒤 LLM을 통해 10~20개의 일반화된 재표현 규칙(Rephrasing Rules)을 증류하고, 추론 시 정책 모델 수정 없이 입력 지시문을 1회 재작성함으로써 제로샷으로 성능을 16~27% 상대 향상시켰다.

## 논문이 해결하는 문제
최신 VLA 모델(예: Physical Intelligence의 $\pi_0$, $\pi_{0.5}$)은 인터넷 규모의 텍스트-이미지 코퍼스로 사전학습된 VLM 백본을 채택하고 있음에도 불구하고, 로봇 제어 정책(Policy)으로 파인튜닝되는 과정에서 심각한 언어적 취약성을 드러냅니다. 예를 들어 LIBERO 벤치마크 환경에서 $\pi_{0.5}$는 "switch on the stove"라는 지시문에 대해서는 100% 성공률을 기록하지만, 의미적으로 완전히 동일한 "switch on the hot plate"에 대해서는 성공률이 2%로 폭락합니다. 심지어 학습 단계에서 다양한 패러프레이징 데이터 증강(Rephrase Augmentation)을 거친 $\pi_0$ 체크포인트조차 최대 61%p에 달하는 성능 편차를 보입니다.

본 논문은 이러한 VLA의 언어 민감성을 통계적으로 엄밀하게 규명하고, 파라미터 재학습(Retraining)이나 매 타임스텝마다의 비싼 검증 루프(Per-step Verification) 없이 순수 추론 전처리(Pre-act rewriting) 관점에서 이를 해결하고자 합니다.

## 기존 방법의 한계
1. **데이터 증강(Data Augmentation)의 불완전성**: 학습 단계에서 LLM을 이용해 지시문을 다변화하여 증강하더라도, 연속적인 행동 제어 공간(Continuous Action Space)으로 매핑되는 VLA의 잠재 공간(Latent Space)에서 언어 임베딩의 극심한 비등방성(Anisotropy)과 국소적 민감성(Local Sensitivity)이 완벽히 해소되지 않습니다.
2. **사전학습 표현의 불일치(Representational Drift)**: VLM 백본이 지닌 방대한 상식 및 언어 강건성이 소규모 로봇 궤적(Robot Trajectory) 데이터셋을 모방 학습(Imitation Learning)하는 과정에서 파괴되거나 특정 토큰 분포에 과적합(Overfitting)됩니다.
3. **높은 재학습 비용 및 파이프라인 복잡도**: 모델 파라미터를 다시 학습시키는 것은 막대한 연산 자원을 소모하며, 런타임에 다수의 후보 행동을 샘플링하고 검증하는 방식(Test-time Verification)은 실시간 제어(예: 10Hz~50Hz)가 필수적인 로봇 환경에 심각한 지연 시간(Latency)을 초래합니다.

## 핵심 기여
1. **언어 민감성의 정량적·통계적 특성화**: 단일 단어 편집(Single-edit Swings) 실험과 가설 검정을 통해 VLA의 성능 급락이 통계적으로 유의미함을 입증하고, 오라클 프레이즈 검색(Oracle Phrase Search)을 통해 적절한 언어 지시문 선택만으로 OOD 태스크 성능 저하(21%p)를 상쇄할 수 있음을 규명했습니다.
2. **규칙 기반 재표현 프레임워크(Distilled Rule-based Rephrasing)**: 소수의 학습 태스크에서 생성된 다양한 표현 평가 결과를 LLM에 제공하여 10~20개의 간결한 자연어 변환 규칙을 증류(Distill)하는 경량화 파이프라인을 고안했습니다.
3. **비침습적 제로샷 일반화(Zero-shot & Model-agnostic)**: 로봇 정책 파라미터를 동결(Frozen)한 채, 유입되는 자연어 명령을 배포 시 1회 재작성하는 것만으로 $\pi_0$와 $\pi_{0.5}$, LIBERO 벤치마크 및 12개의 비공개 태스크 전반에서 일관된 성능 향상(상대 16~27%)을 달성했습니다.

## 제안 방법과 주요 수식

### 1. 단일 편집 민감도(Single-Edit Sensitivity) 및 오라클 격차 정량화
지시문 집합 $\mathcal{U} = \{u_1, u_2, \dots, u_K\}$가 주어졌을 때, 태스크 $\tau$에 대한 VLA 정책 $\pi_\theta$의 성공 확률을 $S(\pi_\theta, u, \tau) \in [0, 1]$로 정의합니다. 기존 명목 지시문(Nominal prompt) $u_{\text{nom}}$과 단일 토큰/구문이 편집된 $u'$ 간의 성능 편차 $\Delta S$는 다음과 같습니다:

$$
\Delta S(u_{\text{nom}}, u') = |S(\pi_\theta, u_{\text{nom}}, \tau) - S(\pi_\theta, u', \tau)|
$$

논문에서는 이 차이가 베르누이 시행 하에서 단순 샘플링 오차가 아님을 검정하기 위해 피셔의 정확 검정(Fisher's Exact Test) 및 부트스트래핑 신뢰구간(Bootstrap Confidence Intervals)을 적용합니다.

오라클 표현 검색(Oracle Search)은 주어진 후보군 $\mathcal{U}_\tau$ 내에서 정책 성능을 극대화하는 상한선을 측정합니다:

$$
u^*_\tau = \arg\max_{u \in \mathcal{U}_\tau} S(\pi_\theta, u, \tau)
$$

실험적으로 OOD 태스크 집합 $\mathcal{T}_{\text{OOD}}$와 ID 태스크 집합 $\mathcal{T}_{\text{ID}}$ 간의 성능 차이는 $u_{\text{nom}}$ 하에서는 명확하지만, 오라클 표현 $u^*$ 하에서는 다음과 같이 거의 소멸합니다:

$$
\mathbb{E}_{\tau \in \mathcal{T}_{\text{ID}}}[S(\pi_\theta, u^*_\tau, \tau)] - \mathbb{E}_{\tau \in \mathcal{T}_{\text{OOD}}}[S(\pi_\theta, u^*_\tau, \tau)] \approx 0
$$

### 2. 재표현 규칙 증류(Distilling Rephrasing Rules via LLM)
본 프레임워크는 정책 $\pi_\theta$의 파라미터를 수정하지 않고, 변환 함수 $f_\phi: \mathcal{U} \to \mathcal{U}$를 최적화합니다. 변환 함수는 대형 언어 모델(LLM)과 규칙 집합 $\mathcal{R} = \{r_1, r_2, \dots, r_M\}$ ($M \approx 10 \sim 20$)의 결합으로 구현됩니다.

1. **경험적 증거 수집(Empirical Profiling)**: 파인튜닝 데이터셋에서 샘플링한 소수의 기준 태스크 $\mathcal{T}_{\text{train\_eval}}$에 대해 LLM을 사용해 의미 보존적 변형 세트 $\mathcal{U}_\tau$를 생성하고, 환경에서 롤아웃을 수행하여 경험적 성공률 $S(\pi_\theta, u, \tau)$를 측정합니다.
2. **패턴 증류 프롬프트(LLM Meta-Prompting)**: 각 태스크별 고성능 표현 집합 $\mathcal{U}^+_\tau$과 저성능 표현 집합 $\mathcal{U}^-_\tau$을 LLM 콘텍스트로 전달하여 고빈도 실패 유발 구문(Failure Modes)과 성공 유도 패턴(Success Idioms)을 추출합니다:

$$
\mathcal{R} \sim P_{\text{LLM}}\left(\mathcal{R} \;\middle|\; \{(\mathcal{U}^+_\tau, \mathcal{U}^-_\tau, \tau)\}_{\tau \in \mathcal{T}_{\text{train\_eval}}}\right)
$$

증류된 규칙 $\mathcal{R}$은 "단순 명사 대신 동작 대상의 기하학적/물리적 지칭어 선호", "모호한 동사 대체", "전치사구 축약" 등의 형태로 사람이 해석 가능한(Human-interpretable) 텍스트 명제로 구성됩니다.

### 3. 단일 통과 전처리(Single-Pass Pre-Execution Rewriting)
새로운 환경에서 사용자 지시문 $u_{\text{in}}$이 유입되면, 배포 전 단 한 번 LLM을 호출하여 규칙 $\mathcal{R}$을 조건부로 반영한 표준화 지시문 $u_{\text{rewritten}}$을 생성합니다:

$$
u_{\text{rewritten}} = f(u_{\text{in}}; \mathcal{R})
$$

최종적으로 로봇 정책은 보정된 지시문을 바탕으로 실시간 제어를 수행합니다:

$$
a_t \sim \pi_\theta(a_t \mid o_t, u_{\text{rewritten}})
$$

이 구조는 액션 추론 루프 외부에 위치하므로 고빈도 제어(Control loop)에 부하를 주지 않습니다.

## 핵심 구조

```
[User Input Instruction (u_in)]
           │
           ▼
┌──────────────────────────────────────────────┐
│  LLM Rewriter with Distilled Rules (R)       │
│  (10~20 Interpretable Rephrasing Rules)       │
└──────────────────────────────────────────────┘
           │
           ▼
[Standardized Instruction (u_rewritten)]
           │
           ▼
┌──────────────────────────────────────────────┐
│  Frozen Vision-Language-Action Policy (π_θ)   │
│  (e.g., π_0, π_0.5 with Visual Input o_t)     │
└──────────────────────────────────────────────┘
           │
           ▼
[Low-Level Action Trajectory (a_t)]
```

*시각 자료 참고 (논문 내 핵심 개요도):*
논문의 **Figure 1**은 제안된 파이프라인의 전체 워크플로우를 요약하고 있습니다. 
- 상단부(Offline Phase)는 소수 태스크의 파라프레이징 성공/실패 궤적 데이터를 수집하여 LLM을 통해 10~20개의 일반화된 재표현 규칙 $\mathcal{R}$을 자동 도출하는 증류 단계를 나타냅니다.
- 하단부(Online Phase)는 사용자의 임의 지시문이 입력되었을 때, 증류된 규칙을 바탕으로 LLM이 단 1회 지시문을 정규화한 뒤, 동결된 VLA 정책($\pi_0 / \pi_{0.5}$)에 공급하여 최종 로봇 모션을 제어하는 비침습적 추론 구조를 상세히 시각화하고 있습니다.

## 실험 설정과 결과

### 1. 벤치마크 및 모델
- **대상 모델**: Physical Intelligence의 $\pi_0$ (재표현 증강 포함 버전 포함), $\pi_{0.5}$.
- **평가 환경**: LIBERO 시뮬레이션 벤치마크 및 12개의 비공개 평가 태스크 (Held-out tasks).
- **테스트 프롬프트 범주**: 적대적 표현(Adversarial), VLM 생성 표현(VLM-generated), 실제 사용자 표현(Human-generated).

### 2. 정량적 결과
- **단일 편집 취약성 검증**: $\pi_{0.5}$ 모델에서 "switch on the stove"는 100% 성공한 반면 "switch on the hot plate"는 2%로 98%p 급락. 증강 학습된 $\pi_0$ 역시 특정 구문 변경 시 최대 61%p의 편차를 보임.
- **오라클 표현의 잠재력**: 명목 프롬프트 기준 ID 대비 OOD 성능 격차는 21%p에 달했으나, 표현 검색(Oracle Search)을 통과한 지시문 사용 시 이 격차가 거의 0에 수렴.
- **규칙 기반 재표현의 성능 향상**:
  - 동결된 $\pi_0$ 기준 12개 Held-out 태스크 전반에서 **16% ~ 27%의 상대적 성공률 향상** 달성.
  - 개선 효과는 특히 훈련 분포를 벗어난 OOD 태스크에서 더욱 두드러짐.
  - $\pi_{0.5}$를 적용한 LIBERO 파인튜닝 실험에서 기본 성공률 93.6%를 **97.8%**로 끌어올림.

## 잘한 점
- **근본적 결함의 명확한 실증**: VLM 기반 로보틱스 연구에서 간과되던 "VLM의 언어 이해력 상실(Catastrophic linguistic degradation)" 현상을 정밀한 단일 편집 대조군 실험을 통해 반박 불가하게 입증했습니다.
- **극단적인 실용성과 비용 효율성**: 파인튜닝 비용이 매우 높은 최신 대규모 VLA 모델을 전혀 재학습하지 않고, 추론 시점의 액션 레이턴시를 100% 보존하면서 오프라인 규칙 증류만으로 안정성을 확보했습니다.
- **해석 가능성(Interpretability)**: 블랙박스 프롬프트 튜닝(Soft Prompting)이나 잠재 벡터 조작 대신, 인간이 읽고 검증할 수 있는 자연어 형태의 10~20개 명시적 규칙으로 취약점을 구조화했습니다.

## 한계와 의문점
- **LLM 추론 의존성**: 실시간 제어 루프 진입 전 1회에 불과하더라도, 초기 태스크 초기화 시점에 LLM API 호출 또는 로컬 LLM 추론에 따른 수백 ms의 콜드 스타트 지연(Initial Latency)이 발생합니다.
- **시각적 맥락 미반영(Unimodal Rewriting)**: 재표현 규칙 적용 단계에서 현재 카메라 뷰(Vision input)를 고려하지 않고 텍스트 레벨에서만 재작성하므로, 시각적 모호성(예: 동일 물체가 두 개 존재하는 상황)에 기인한 지시문 실패는 교정하기 어렵습니다.
- **규칙 세트의 VLA 아키텍처 의존성**: 특정 백본($\pi_0$)에서 도출된 재표현 선호 규칙이 다른 구조(예: OpenVLA, Octo 등)나 다른 VLM 백본(PaliGemma vs Llama)에도 일관되게 전이(Transfer)되는지 명확한 한계가 존재합니다.

## 실무 적용 가능성
- **프로덕션 로봇 시스템의 즉각적 보호막(Safety Guardrail)**: 실제 서비스 배포 환경에서 불특정 다수의 고객이 입력하는 자연어 변형(사투리, 비표준어, 다양한 유의어)을 정규화하는 게이트웨이(Gateway) 모듈로 즉시 투입할 수 있습니다.
- **데이터 엔지니어링 비용 절감**: 파인튜닝 궤적 데이터의 지시문 레이블을 전수 재작업하거나 천문학적인 비용으로 데이터 증강 정책을 학습시키는 대신, 소규모 태스크 분석만으로 정책의 수명과 범용성을 극대화할 수 있습니다.

## 관련 연구와 연결점
- **VLA 기반 모델**: Physical Intelligence의 $\pi_0$ / $\pi_{0.5}$, OpenVLA, Octo 등 로봇 매니퓰레이션 모델이 직면한 모달리티 불일치 문제와 직결됩니다.
- **자연어 처리의 프롬프트 엔지니어링 및 캘리브레이션**: LLM 분야의 Prompt Rewriting 및 Instruction Standardization 기법이 로보틱스 행동 공간 안정화로 확장된 사례입니다.

## 원문 정보
- Title: Rephrase Before You Act: Characterizing and Mitigating Language Sensitivity in Vision-Language-Action Models
- Authors: Mikey Watts, Yuchen Cui
- Venue/Repository: arXiv
- Published: 2026-10 (arXiv pre-print: 2610.10526v1)
- URL: https://arxiv.org/abs/2610.10526

> 이 글은 자동 생성된 초안을 바탕으로 작성되며, 공개 전에 저자·수식·수치·출처를 직접 검수합니다.
```