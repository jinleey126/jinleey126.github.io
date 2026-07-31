---
title: "Diffusion의 Markov Chain과 Forward·Reverse Process"
description: "DDPM의 Markov property, noise schedule과 alpha notation을 바탕으로 forward process와 학습 가능한 reverse process를 정리한다."
date: 2026-01-09 09:00:00 +0900
categories:
  - Paper Reviews
  - Multimodal
tags:
  - Diffusion
  - DDPM
  - Markov Chain
  - Noise Schedule
toc: true
math: true
---

## 0. 체크리스트

아래 질문들에 대해 답변할 수 있다면 해당 포스트는 바로 넘어가도 된다.

- Markov property는 무엇인가?
- $\beta_t$, $\alpha_t$, $\bar\alpha_t$는 각각 무엇을 의미하는가?
- $x_0$에서 임의의 $x_t$를 한 번에 샘플링할 수 있는 이유는 무엇인가?
- forward process와 reverse process 중 어느 쪽을 학습하는가?

---

## 1. Markov Property

Markov chain에서는 현재 상태가 주어지면 다음 상태가 과거 전체와 조건부 독립이다.

$$
q(x_t\mid x_{0:t-1})
=
q(x_t\mid x_{t-1})
$$

즉, $x_t$를 만들 때 $x_0,\ldots,x_{t-2}$를 모두 확인할 필요 없이 바로 이전 상태 $x_{t-1}$만 사용한다.

Diffusion의 forward process도 다음과 같은 Markov chain이다.

$$
x_0
\rightarrow
x_1
\rightarrow
\cdots
\rightarrow
x_T
$$

각 단계에서는 바로 이전 이미지에 소량의 Gaussian noise를 추가한다.

<br/>

## 2. Forward Process와 Noise Schedule

한 단계의 forward transition은 다음과 같이 정의한다.

$$
q(x_t\mid x_{t-1})
=
\mathcal N
\left(
\sqrt{1-\beta_t}x_{t-1},
\beta_t I
\right)
$$

여기서 $\beta_t$는 timestep $t$에서 추가하는 noise의 분산이다.

- $\beta_t$가 작으면 한 단계에서 원본 신호가 조금만 감소한다.
- $\beta_t$가 크면 한 단계에서 더 많은 noise가 추가된다.
- timestep별 $\beta_t$의 집합을 noise schedule이라고 한다.

Forward process는 사람이 미리 정한 $\beta_t$에 의해 결정되며 학습하지 않는다.

<br/>

## 3. Alpha Notation

식을 단순하게 표현하기 위해 다음 값을 정의한다.

$$
\alpha_t=1-\beta_t
$$

$$
\bar\alpha_t
=
\prod_{s=1}^{t}\alpha_s
$$

$\alpha_t$는 한 단계에서 유지되는 신호의 비율이고, $\bar\alpha_t$는 $x_0$에서 timestep $t$까지 누적해서 유지되는 신호의 비율이다.

Reparameterization을 적용하면 한 단계 transition을 다음처럼 표현할 수 있다.

$$
x_t
=
\sqrt{\alpha_t}x_{t-1}
+
\sqrt{1-\alpha_t}\epsilon_t,
\qquad
\epsilon_t\sim\mathcal N(0,I)
$$

이를 반복해서 전개하면 다음 closed-form을 얻는다.

$$
q(x_t\mid x_0)
=
\mathcal N
\left(
\sqrt{\bar\alpha_t}x_0,
(1-\bar\alpha_t)I
\right)
$$

따라서 $x_t$는 다음처럼 직접 샘플링할 수 있다.

$$
x_t
=
\sqrt{\bar\alpha_t}x_0
+
\sqrt{1-\bar\alpha_t}\epsilon,
\qquad
\epsilon\sim\mathcal N(0,I)
$$

이 식 덕분에 학습할 때 $x_1,\ldots,x_{t-1}$을 순서대로 생성하지 않고 $x_0$에서 원하는 $x_t$로 바로 이동할 수 있다.

<br/>

## 4. Reverse Process

생성 과정은 forward process의 반대 방향으로 진행한다.

$$
x_T
\rightarrow
x_{T-1}
\rightarrow
\cdots
\rightarrow
x_0
$$

Reverse transition은 학습 가능한 Gaussian distribution으로 정의한다.

$$
p_\theta(x_{t-1}\mid x_t)
=
\mathcal N
\left(
\mu_\theta(x_t,t),
\Sigma_\theta(x_t,t)
\right)
$$

신경망은 noisy image $x_t$와 timestep $t$를 입력받아 reverse distribution의 파라미터를 예측한다.

실제 DDPM 구현에서는 평균 $\mu_\theta$를 직접 예측하는 대신 $x_t$에 추가된 noise를 예측하는 경우가 많다.

$$
\epsilon_\theta(x_t,t)
$$

예측한 noise를 이용하면 원본 $x_0$의 추정값이나 reverse mean을 계산할 수 있다.

<br/>

## 5. 꼭 구분할 것

| 구분 | Forward Process | Reverse Process |
|---|---|---|
| 방향 | 데이터 $\rightarrow$ noise | noise $\rightarrow$ 데이터 |
| 분포 | $q(x_t\mid x_{t-1})$ | $p_\theta(x_{t-1}\mid x_t)$ |
| 파라미터 | noise schedule로 고정 | 신경망으로 학습 |
| 학습 시 역할 | noisy input 생성 | 추가된 noise 또는 reverse mean 예측 |

### 확인 문제

학습할 때 $x_0$에서 $x_t$를 한 번에 만들 수 있는 이유를 설명해보자.

답:<br/>
Gaussian transition을 반복해서 합성한 $q(x_t\mid x_0)$의 closed-form을 알고 있기 때문이다. 따라서 $\bar\alpha_t$와 하나의 Gaussian noise $\epsilon$만으로 원하는 timestep의 $x_t$를 직접 샘플링할 수 있다.
