---
title: "SLICE: Sequential Likelihood-Free Inference via Conformal E-Values"
description: "시뮬레이터 기반 모델에서 우도 계산 없이 Conformal E-value와 검정 마팅게일을 결합하여 언제든 유효한(anytime-valid) 모수 신뢰 시퀀스를 구성하는 방법론을 제시합니다."
date: 2026-10-24 09:00:00 +0900
categories:
  - Paper Reviews
  - uncertainty-quantification
paper_authors:
  - Stefano Cortinovis
  - Laura Battaglia
  - François Caron
paper_url: "https://arxiv.org/abs/2610.13855v1"
tags:
  - Likelihood-Free Inference
  - Conformal Prediction
  - E-values
  - Test Martingale
  - Confidence Sequences
toc: true
mermaid: false
---

## 3줄 요약

- 우도 함수(Likelihood)의 계산이 불가능하고 순방향 시뮬레이션만 가능한 환경에서, 임의의 시점에 데이터를 조기 종료·연속 모니터링하더라도 1종 오류율이 수학적으로 엄밀히 보장되는 언제든 유효한(anytime-valid) 신뢰 시퀀스(Confidence Sequence)를 구축했습니다.
- 각 관측 시점마다 귀무가설 모수에서 생성한 신선한(fresh) 시뮬레이션 표본들의 교환가능성(exchangeability)을 활용하여 점수 함수(score function)를 Conformal e-value로 변환하고, 이를 곱해 검정 마팅게일(test martingale)을 형성한 뒤 파라미터 공간에 대해 반전(inversion)합니다.
- 점수 함수의 형태나 신경망 근사 오차의 크기와 무관하게 유한 표본 커버리지가 무조건 성립하며, 신경망 기반 우도비 추정기(Neural Ratio Estimator)를 활용해 로그 성장률 최적성(Growth-Rate Optimality)에 근접하는 효율적인 신뢰 영역 수축을 달성했습니다.

## 논문이 해결하는 문제

천체물리학, 생태학, 전염병학, 금융 및 거대 언어 모델(LLM) 시스템 등 복잡한 실세계 현상은 결정론적 수식으로 우도 함수 $p(x \mid \theta)$를 닫힌 형식(closed-form)으로 유도하기 어렵지만, 컴퓨터 시뮬레이터를 통해 모수 $\theta$로부터 관측 데이터 $x \sim p(\cdot \mid \theta)$를 무한히 생성할 수 있는 시뮬레이션 기반 추론(Simulation-Based Inference, SBI) 또는 가능도 부재 추론(Likelihood-Free Inference, LFI) 환경에 놓여 있는 경우가 많습니다.

이러한 환경에서 빈도주의적 불확실성 정량화(Frequentist Uncertainty Quantification)를 수행할 때 발생하는 핵심 과제는 다음과 같습니다:

1. **연속 모니터링과 다중 검정(Multiple Testing / Peeking Problem):** 데이터가 실시간 스트리밍으로 유입될 때 연구자나 시스템 감사자(auditor)는 고정된 표본 수에 도달하기 전에 임의의 시점에 결과를 들여다보고 결정을 내리거나 실험을 조기 종료(optional stopping)하길 원합니다. 전통적인 신뢰구간은 이 경우 1종 오류가 급격히 팽창합니다.
2. **시뮬레이터 기반 환경에서의 유한 표본 보증 부재:** 심층 신경망을 활용한 최신 SBI 방법론(NPE, NRE 등)은 신경망의 학습 오차, 일반화 갭, 모델 미스스펙으로 인해 점근적(asymptotic) 통계 보증만 제공할 뿐 유한 표본(finite-sample)에서의 정확한 신뢰구간을 보장하지 못합니다.

본 논문은 이 두 문제를 동시에 해결하여, LFI 환경에서 임의의 중단 규칙(arbitrary stopping rule) 하에서도 유한 표본 오차율이 엄밀히 제어되는 **언제든 유효한 신뢰 시퀀스(Anytime-Valid Confidence Sequences)**를 도출하는 프레임워크인 **SLICE(Sequential Likelihood-Free Inference via Conformal E-Values)**를 제안합니다.

## 기존 방법의 한계

- **고정 표본 크기 가정(Fixed-Sample Size Assumption):** 기존의 LFI 기반 Conformal Prediction 연구들은 표본 크기 $N$이 사전에 정해져 있다고 가정합니다. 데이터가 순차적으로 들어오는 환경에서 고정 표본 conformal $p$-value를 지속해서 모니터링하면, 다중 검정 문제로 인해 명목 신뢰 수준 $1-\alpha$가 깨집니다.
- **점근적 정규성 및 피셔 정보량 근사 의존:** 합성 우도(synthetic likelihood)나 Wald/Score 검정에 기반한 시뮬레이션 기반 추론은 표본 수가 무한대로 갈 때 중심극한정리(CLT)가 성립한다는 점근적 가정에 의존합니다. 표본 수가 작거나 우도 표면이 비정규적인 경우 커버리지 왜곡이 심각합니다.
- **신경망 근사 품질에 대한 취약성:** Neural Posterior Estimation(NPE)이나 Neural Ratio Estimation(NRE)은 신경망이 사후확률이나 우도비를 완벽히 근사했다고 가정합니다. 근사 편향(bias)이 발생하면 불확실성이 과소평가(overconfident)되는 치명적인 문제가 존재하지만, 이를 사후적으로 유한 표본에서 교정하는 순차적 방법은 부재했습니다.

## 핵심 기여

1. **LFI를 위한 Conformal E-value 및 마팅게일 구축:** 각 시점 $t$마다 귀무가설 $\theta_0$에서 생성된 $K$개의 독립 시뮬레이션 표본과 실제 관측치 간의 교환가능성(exchangeability)을 활용하여 유효한 조건부 E-value(conditional e-value)를 구성하고, 이들의 누적 곱으로 검정 마팅게일(test martingale)을 정의했습니다.
2. **신경망 오차에 무관한 엄밀한 유한 표본 커버리지:** 임의의 예측 점수 함수(predictable score function) $s_t(x) > 0$에 대해, 점수 함수의 예측력이나 신경망 추정기의 정확도와 상관없이 빌의 부등식(Ville's inequality)에 의해 모든 시점에서 $1-\alpha$ 유효성이 성립함을 증명했습니다.
3. **정보 이론적 최적성(GRO)과 신경망 우도비 추정의 연계:** 신뢰 시퀀스의 수축 속도를 극대화하는 최적 점수 함수가 오라클 우도비(likelihood ratio)임을 로그 성장률 최적성(Growth-Rate Optimality, GRO) 관점에서 규명하고, 이를 사전 학습된 분할 상환 신경망 우도비 추정기(Amortized Neural Ratio Estimator)로 근사하는 실용적 구조를 제안했습니다.
4. **다양한 영역에서의 실증:** 합성 LFI 벤치마크, LLM API의 실시간 모델 라우팅 감사(model routing audit), 천체물리학 중력 마이크로렌징(gravitational microlensing) 관측 데이터에서 고정 표본 방법 대비 우월한 순차 검정 유효성과 효율성을 입증했습니다.

## 제안 방법과 주요 수식

### 1. Conformal E-Values 구성

모수 공간 $\Theta$에 대해 단일 귀무가설 $H_0: \theta = \theta_0$를 순차적으로 검정하는 문제를 고려합니다. 시점 $t \in \{1, 2, \dots\}$에서 실제 환경으로부터 관측치 $X_t \sim P_{\theta^*}$가 유입됩니다. 동시에, 분석가는 시뮬레이터를 통해 후보 모수 $\theta_0$로부터 $K$개의 독립적인 가상 표본을 새로 추출합니다:

$$Z_{t,1}, Z_{t,2}, \dots, Z_{t,K} \stackrel{\text{i.i.d.}}{\sim} P_{\theta_0}$$

시점 $t$ 이전의 관측 및 시뮬레이션 이력으로 구성된 필트레이션(filtration)을 $\mathcal{F}_{t-1}$이라 할 때, $\mathcal{F}_{t-1}$에 대해 가측(measurable)인 임의의 양수 점수 함수 $s_t: \mathcal{X} \to (0, \infty)$를 정의합니다. 귀무가설 $H_0: \theta^* = \theta_0$ 하에서 관측치 $X_t$와 시뮬레이션 표본 $\{Z_{t,k}\}_{k=1}^K$는 조건부로 상호 교환가능(conditionally exchangeable)합니다.

논문은 Conformal Prediction의 순위 아이디어를 e-value 형태로 확장하여 다음과 같은 Conformal E-Value $E_t(\theta_0)$를 정의합니다:

$$E_t(\theta_0) = \frac{(K+1) s_t(X_t)}{s_t(X_t) + \sum_{k=1}^K s_t(Z_{t,k})}$$

여기서 $X_t$와 $Z_{t,k}$의 대칭성에 의해, 귀무가설 하에서 조건부 기댓값은 정확히 1이 됩니다:

$$\mathbb{E}\left[ E_t(\theta_0) \;\middle|\; \mathcal{F}_{t-1} \right] = \frac{K+1}{K+1} = 1$$

따라서 $E_t(\theta_0)$는 임의의 점수 함수 $s_t$에 대해 유효한 조건부 e-value입니다.

### 2. 검정 마팅게일(Test Martingale)과 빌의 부등식(Ville's Inequality)

시점 $t$까지의 누적 검정 통계량 $M_t(\theta_0)$를 e-value들의 누적 곱으로 정의합니다:

$$M_t(\theta_0) = \prod_{i=1}^t E_i(\theta_0), \quad M_0(\theta_0) = 1$$

$\mathbb{E}[M_t(\theta_0) \mid \mathcal{F}_{t-1}] = M_{t-1}(\theta_0) \mathbb{E}[E_t(\theta_0) \mid \mathcal{F}_{t-1}] = M_{t-1}(\theta_0)$이 성립하므로, $M_t(\theta_0)$는 비음수 마팅게일(non-negative martingale)입니다.

빌의 최대 부등식(Ville's maximal inequality)을 적용하면 임의의 유의수준 $\alpha \in (0, 1)$에 대해 다음이 성립합니다:

$$\mathbb{P}_{\theta_0} \left( \exists t \ge 1 : M_t(\theta_0) \ge \frac{1}{\alpha} \right) \le \alpha$$

### 3. 신뢰 시퀀스(Confidence Sequence) 도출

모수 공간 전체 $\Theta$에 대해 귀무가설 검정을 반전(inverting the sequential test)시킴으로써, 언제든 유효한 신뢰 시퀀스 $C_t$를 구축합니다:

$$C_t = \left\{ \theta \in \Theta : M_t(\theta) < \frac{1}{\alpha} \right\} = \left\{ \theta \in \Theta : \prod_{i=1}^t \frac{(K+1) s_i(X_i; \theta)}{s_i(X_i; \theta) + \sum_{k=1}^K s_i(Z_{i,k}^{(\theta)}; \theta)} < \frac{1}{\alpha} \right\}$$

이 신뢰 시퀀스는 임의의 정지 시간(stopping time) $\tau$에 대해 다음의 통일된 신뢰 수준을 완벽히 보장합니다:

$$\mathbb{P}_{\theta^*} \left( \forall t \ge 1, \; \theta^* \in C_t \right) \ge 1 - \alpha$$

### 4. 로그 성장률 최적화(GRO)와 Amortized NRE 점수 함수

신뢰 시퀀스의 부피가 빠르게 줄어들기 위해서는 참 모수 $\theta^*$와 대립하는 잘못된 모수 $\theta \neq \theta^*$에 대해 $M_t(\theta)$가 가능한 한 빠르게 무한대로 발산해야 합니다. 즉, 대립가설 하에서 기대 로그 성장률 $\mathbb{E}_{\theta^*}[\log E_t(\theta)]$을 극대화해야 합니다.

오라클 설정에서 대립가설 분포 $P_{\theta^*}$와 귀무분포 $P_{\theta}$의 라돈-니코딤 도함수(우도비) $r^*(x) = \frac{p(x \mid \theta^*)}{p(x \mid \theta)}$를 점수 함수로 취할 때:

$$s^*(x; \theta) = \frac{p(x \mid \theta^*)}{p(x \mid \theta)}$$

이 점수 함수는 Kelly 베팅 원리에 따라 기대 로그 성장률을 점근적으로 극대화합니다(Growth-Rate Optimal, GRO). 우도비가 해석적으로 주어지지 않는 LFI 환경이므로, 저자들은 사전 훈련(offline pre-training) 단계에서 신경망 분류기를 이진 교차 엔트로피(BCE) 손실함수로 학습시키는 Amortized Neural Ratio Estimation(NRE)을 사용합니다:

$$\mathcal{L}(\phi) = -\mathbb{E}_{(\theta, \theta', x) \sim p(\theta)p(\theta')p(x \mid \theta')} \left[ \log \sigma(f_\phi(x, \theta, \theta')) \right] - \mathbb{E}_{(\theta, x) \sim p(\theta)p(x \mid \theta)} \left[ \log (1 - \sigma(f_\phi(x, \theta, \theta))) \right]$$

신경망으로 추정된 우도비 $\hat{r}_\phi(x; \theta) \approx \frac{p(x \mid \hat{\theta}_{MLE})}{p(x \mid \theta)}$를 점수 함수 $s_t(x; \theta)$로 대입합니다. **핵심은 $\hat{r}_\phi$에 근사 오차가 아무리 크더라도, Conformal E-value 수식 자체의 대칭성 덕분에 신뢰 시퀀스의 $1-\alpha$ 유효성은 수학적으로 절대 깨지지 않는다는 점입니다.**

## 핵심 구조

```
[오프라인 사전 단계 (Offline Phase)]
┌────────────────────────────────────────────────────────┐
│ 시뮬레이터 샘플링: (θ, x) ~ p(θ)p(x|θ)                 │
│ 신경망 우도비 추정기 학습: f_φ(x, θ, θ')                │
│ -> 점수 함수 s(x; θ) 확보 (추정 오차가 있어도 무방)    │
└────────────────────────────────────────────────────────┘
                           │
                           ▼
[온라인 순차 추론 단계 (Online Sequential Inference)]
시점 t = 1, 2, 3, ... (데이터 스트림)
  │
  ├─► 실제 관측 데이터 유입: X_t ~ P_θ*
  │
  ├─► 모수 공간 그리드 θ ∈ Θ 순회
  │     │
  │     ├─► 시뮬레이터 구동: Z_{t, 1:K} ~ P_θ (K개 신선한 샘플)
  │     │
  │     ├─► 예측 점수 계산: s_t(X_t; θ), s_t(Z_{t,k}; θ)
  │     │
  │     ├─► Conformal E-Value 산출:
  │     │     E_t(θ) = (K+1) * s_t(X_t) / (s_t(X_t) + Σ s_t(Z_{t,k}))
  │     │
  │     └─► 검정 마팅게일 갱신:
  │           M_t(θ) = M_{t-1}(θ) * E_t(θ)
  │
  └─► 신뢰 시퀀스 도출 (임의 조기 종료 가능):
        C_t = { θ ∈ Θ : M_t(θ) < 1/α }
        * Ville's inequality에 의해 모든 시점 t에서 P(θ* ∈ C_t) ≥ 1 - α 보장
```

*Figure 1 설명 (원문 참조 안내):*
원문의 시스템 아키텍처 및 파이프라인 다이어그램(Figure 1)을 확인하면, 상단의 오프라인 신경망 비율 추정기(Amortized NRE) 학습 블록과 하단의 실시간 순차 데이터 업데이트 루프가 시각적으로 분리되어 있습니다. 온라인 루프에서는 새로운 관측치 $X_t$가 들어올 때마다 후보 모수 공간 상의 각 점 $\theta$에 대해 시뮬레이터가 즉각적으로 $K$개의 가상 데이터를 생성하고, 이를 대입해 Conformal E-value를 계산하는 과정이 묘사됩니다. 

이어 각 모수점의 누적 마팅게일 $M_t(\theta)$ 궤적이 $1/\alpha$ 임계선을 초과하는지 여부에 따라 해당 파라미터가 기각(reject)되어 유효 신뢰 영역 $C_t$에서 제거되는 양상이 2차원 등고선(contour) 및 1차원 궤적 플롯으로 표현되어 있습니다. 사용자는 원문의 Figure 1을 통해 신경망 점수 함수의 근사적 역할과 Conformalization을 통한 엄밀한 1종 오류 제어가 어떻게 결합되는지 전체 데이터 흐름을 직관적으로 파악할 수 있습니다.

## 실험 설정과 결과

### 1. 실험 설정
- **Synthetic SBI 벤치마크:** Gaussian Mixture Model(다중 모드 사후분포), Two Moons(비선형 기하학적 형상), Simple Likelihood-Complex Posterior(SLCP) 모델을 포함.
- **LLM API 모델 라우팅 감사(Audit):** 비용 절감을 위해 상위 모델(예: GPT-4)과 하위 모델(예: GPT-3.5) 간에 동적 라우팅을 수행하는 상용 API에서, 제공자가 계약된 라우팅 비율 $\theta$를 준수하는지 실시간 모니터링. 텍스트 임베딩과 응답 지연 시간 등을 관측 변수로 사용.
- **천체물리학 중력 마이크로렌징(Microlensing):** 중력 렌즈 효과 시뮬레이션 기반 시계열 광도 곡선(light curves) 데이터에서 렌즈 질량 및 기하 모수 추정.
- **비교군:** 고정 표본 분할 conformal prediction, 비순차적 신경망 사후분포 추정(NPE), 오라클 마팅게일 검정.

### 2. 정량적 결과
- **순차 모니터링 시 커버리지 제어:** 
  - 고정 표본 conformal prediction 및 전통적 SBI 신뢰구간은 시점 $t$를 점진적으로 늘려가며 조기 종료를 허용할 때 실증적 커버리지(empirical coverage)가 명목 수준인 95%($\alpha=0.05$)에서 70% 이하로 급격히 붕괴되었습니다.
  - 반면 SLICE는 임의의 중단 시점에서도 모든 벤치마크에서 경험적 오류율을 정확히 $\alpha \le 0.05$ 이하로 엄밀하게 제어했습니다.
- **구간 수축 속도(Efficiency):**
  - 휴리스틱한 거리 기반 점수 함수(예: 유클리드 거리) 대비, Amortized NRE 기반 점수 함수를 장착한 SLICE는 오라클 우도비를 사용한 상한선에 근접하는 로그 성장률을 기록하여, 훨씬 적은 표본 수 $t$만으로 신뢰 시퀀스의 부피를 좁히는 데 성공했습니다.
- **LLM 라우팅 감사:** 서비스 제공자가 은밀히 저가 모델의 비율을 높였을 때, SLICE는 사전 설정된 1종 오류율을 엄격히 유지하면서도 불과 수십 회의 쿼리 샘플링만으로 위반 사실을 통계적으로 유의하게 감지했습니다.

## 잘한 점

1. **완벽한 오류 면책성(Immunity to Approximation Errors):** 심층 신경망을 통계적 검정의 점수 함수로 활용하되, 신경망의 추정 실패(miscalibration, out-of-distribution)가 1종 오류의 붕괴로 이어지지 않도록 Conformal e-value 계층으로 완벽히 격리했습니다.
2. **시뮬레이션 재생성의 창의적 결합:** 일반적인 Conformal Prediction은 과거 캘리브레이션 세트의 크기에 제약을 받지만, LFI 환경의 특성인 "시뮬레이터를 통한 무한 샘플링 가능성"을 활용하여 각 시점 $t$마다 $K$개의 신선한 표본을 독립 생성함으로써 조건부 마팅게일 성질을 우아하게 이끌어냈습니다.
3. **이론과 응용의 균형:** 도박 이론(Kelly betting) 및 마팅게일 통계학의 최신 이론(e-value)을 머신러닝의 실질적인 문제(LLM API 감사, 과학 시뮬레이터 추론)에 적재적소로 결합했습니다.

## 한계와 의문점

1. **고차원 모수 공간에서의 그리드 계산 비용:** 신뢰 시퀀스 $C_t = \{\theta : M_t(\theta) < 1/\alpha\}$를 구하기 위해서는 후보 모수 $\theta$들에 대해 병렬적으로 검정을 수행해야 합니다. 모수 공간 $\Theta$의 차원이 5~10차원 이상으로 증가할 경우, 모수 공간을 이산화(grid discretization)하거나 최적화 기반으로 경계를 탐색하는 비용이 지수적으로 증가(Curse of Dimensionality)합니다.
2. **시뮬레이터 호출 비용 문제:** 각 시점 $t$마다, 각 후보 모수 $\theta$에 대해 $K$개의 새로운 시뮬레이션 $Z_{t,1:K}$를 수행해야 합니다. 시뮬레이터 1회 실행에 수 분 이상 걸리는 대규모 수치해석 시뮬레이션(예: 기후 모델, 유체역학)의 경우 계산 병목이 심각할 수 있습니다.
3. **유한한 $K$로 인한 로그 성장률 손실:** e-value의 이론적 최댓값은 $(K+1)$로 상한이 제한(bounded)됩니다. $K$가 너무 작으면 대립가설을 기각하는 속도가 느려져 탐지 지연(detection delay)이 발생할 수 있습니다.

## 실무 적용 가능성

- **AI 안전성 및 LLM API SLA 감사:** 본 논문에서 제시한 것처럼 상용 파운데이션 모델 서비스 기업이 내부적으로 지연 시간이나 토큰 비용을 낮추기 위해 동적 라우팅(speculative decoding, model cascading)을 수행할 때, 기업 간 SLA 계약 위반이나 무단 다운그레이드를 모니터링하는 서드파티 감사 솔루션에 즉각 도입될 수 있습니다.
- **임상 시험 및 A/B 테스트의 조기 종료:** 시뮬레이션 모델에 기반하여 환자 반응이나 사용자 전환율을 온라인으로 추적하면서, 부작용 발생이나 확실한 승자가 감지되는 즉시 실험을 윤리적·경제적으로 조기 종료하는 의사결정 파이프라인에 최적입니다.

## 관련 연구와 연결점

- **E-values and Anytime-Valid Inference:** Shafer (2021)의 검정 마팅게일 이론, Howard et al. (2021)의 신뢰 시퀀스 기초 이론, Ramdas et al. (2023)의 게임 이론적 통계학 흐름을 직접적으로 계승합니다.
- **Conformal Prediction:** Vovk et al. (2005)의 순차적 conformal prediction 프레임워크를 기반으로 하되, 비음수 마팅게일 e-value 형태로 변환하여 $p$-value 결합 시 발생하는 복잡한 보정(alpha spending) 없이 자연스러운 곱셈 업데이트를 가능하게 했습니다.
- **Neural Simulation-Based Inference:** Cranmer et al. (2020)의 SBI 서베이, Hermans et al. (2020)의 AALR(Amortized Approximate Likelihood Ratio) 기법을 핵심 엔진으로 채택하여 검정력(power)을 확보했습니다.

## 원문 정보

- Title: SLICE: Sequential Likelihood-Free Inference via Conformal E-Values
- Authors: Stefano Cortinovis, Laura Battaglia, François Caron
- Venue/Repository: arXiv
- Published: 2026 (arXiv preprint)
- URL: [https://arxiv.org/abs/2610.13855v1](https://arxiv.org/abs/2610.13855v1)

> 이 글은 자동 생성된 초안을 바탕으로 작성되며, 공개 전에 저자·수식·수치·출처를 직접 검수합니다.