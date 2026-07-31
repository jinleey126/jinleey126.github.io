---
title: "Diffusion 모델 학습을 위한 기대값, Likelihood와 KL Divergence"
description: "Diffusion 학습 목적함수를 이해하기 위해 필요한 기대값, maximum likelihood, negative log-likelihood와 KL divergence를 정리한다."
date: 2026-01-05 09:00:00 +0900
categories:
  - Paper Reviews
  - Multimodal
tags:
  - Diffusion
  - Expectation
  - Likelihood
  - KL Divergence
toc: true
math: true
---

## 0. 체크리스트

아래 질문들에 대해 답변할 수 있다면 해당 포스트는 바로 넘어가도 된다.

- 기대값과 미니 배치 평균은 어떤 관계인가?
- likelihood를 최대화한다는 것은 무엇을 의미하는가?
- KL divergence는 무엇을 측정하며, 왜 거리가 아닌가?
- Gaussian의 분산이 고정되어 있을 때 KL divergence는 어떤 문제로 단순화되는가?

---

## 1. 기대값

확률변수 $x$가 분포 $p(x)$를 따를 때 함수 $f(x)$의 기대값은 다음과 같다.

$$
\mathbb E_{x\sim p(x)}[f(x)]
$$

이는 $p(x)$에서 여러 $x$를 샘플링했을 때 얻는 $f(x)$의 평균을 의미한다.

<br/>

딥러닝에서는 전체 데이터 분포의 기대값을 정확히 계산하는 대신 미니 배치 평균으로 근사한다.

$$
\mathbb E_{x\sim p_{\text{data}}}[f(x)]
\approx
\frac{1}{B}\sum_{i=1}^{B}f(x_i)
$$

여기서 $B$는 미니 배치 크기이다.

<br/>

Diffusion의 noise prediction loss도 기대값으로 표현한다.

$$
\mathcal L_{\text{simple}}
=
\mathbb E_{x_0,t,\epsilon}
\left[
\left\|
\epsilon-\epsilon_\theta(x_t,t)
\right\|^2
\right]
$$

이 식은 다음 과정을 반복해 loss의 평균을 구한다는 뜻이다.

1. 데이터 $x_0$를 샘플링한다.
2. timestep $t$를 샘플링한다.
3. 표준 Gaussian noise $\epsilon$을 샘플링한다.
4. $x_0$, $t$, $\epsilon$을 이용해 noisy image $x_t$를 만든다.
5. 실제 noise $\epsilon$과 예측 noise $\epsilon_\theta(x_t,t)$의 차이를 계산한다.

즉, 하나의 고정된 입력에 대한 오차가 아니라 데이터, timestep과 noise 전반에 대한 평균 오차를 최소화한다.

<br/>

## 2. Maximum Likelihood

생성 모델은 학습 데이터에 높은 확률을 부여하도록 분포 $p_\theta(x)$를 학습한다.

$$
\theta^*
=
\arg\max_\theta
\sum_i \log p_\theta(x_i)
$$

$p_\theta(x_i)$가 커질수록 모델이 실제 데이터 $x_i$를 그럴듯한 샘플로 판단한다는 뜻이다.

여러 확률의 곱 대신 log-likelihood의 합을 사용하는 이유는 다음과 같다.

- 곱을 합으로 바꿔 계산을 단순화한다.
- 매우 작은 확률을 계속 곱할 때 발생하는 수치 불안정을 줄인다.
- 로그 함수는 단조 증가하므로 최댓값의 위치가 바뀌지 않는다.

<br/>

최적화는 일반적으로 목적함수를 최소화하는 방식으로 구현한다. 따라서 log-likelihood에 음수를 붙인 negative log-likelihood를 사용한다.

$$
\mathcal L_{\text{NLL}}
=
-\mathbb E_{x\sim p_{\text{data}}}
\left[
\log p_\theta(x)
\right]
$$

NLL을 줄이는 것은 실제 데이터에 대한 모델의 likelihood를 높이는 것과 같다.

<br/>

## 3. KL Divergence

KL divergence는 두 확률분포 $q$와 $p$가 얼마나 다른지 측정한다.

$$
D_{\mathrm{KL}}(q\|p)
=
\mathbb E_{x\sim q}
\left[
\log\frac{q(x)}{p(x)}
\right]
$$

중요한 성질은 다음과 같다.

$$
D_{\mathrm{KL}}(q\|p)\geq 0
$$

두 분포가 같을 때 KL divergence는 $0$이 된다.

<br/>

하지만 KL divergence는 대칭이 아니다.

$$
D_{\mathrm{KL}}(q\|p)
\neq
D_{\mathrm{KL}}(p\|q)
$$

따라서 일반적인 거리 함수로 볼 수 없다. $D_{\mathrm{KL}}(q\|p)$는 $q$에서 자주 나타나는 영역을 $p$가 얼마나 잘 설명하는지 측정한다.

<br/>

Diffusion에서는 실제 reverse posterior와 학습 가능한 reverse distribution을 가깝게 만드는 데 KL divergence를 사용한다.

$$
D_{\mathrm{KL}}
\left(
q(x_{t-1}\mid x_t,x_0)
\|
p_\theta(x_{t-1}\mid x_t)
\right)
$$

여기서 $q(x_{t-1}\mid x_t,x_0)$는 forward process로부터 계산할 수 있는 분포이고, $p_\theta(x_{t-1}\mid x_t)$는 신경망이 학습해야 하는 분포이다.

<br/>

## 4. Gaussian 사이의 KL Divergence

1차원 Gaussian 분포 두 개를 다음과 같이 정의한다.

$$
q=\mathcal N(\mu_q,\sigma_q^2),
\qquad
p=\mathcal N(\mu_p,\sigma_p^2)
$$

두 분포 사이의 KL divergence는 다음과 같다.

$$
D_{\mathrm{KL}}(q\|p)
=
\log\frac{\sigma_p}{\sigma_q}
+
\frac{\sigma_q^2+(\mu_q-\mu_p)^2}{2\sigma_p^2}
-
\frac{1}{2}
$$

두 분포의 분산이 고정되어 있다면 학습에 따라 달라지는 핵심 항은 평균의 차이이다.

$$
D_{\mathrm{KL}}(q\|p)
\propto
(\mu_q-\mu_p)^2
$$

따라서 KL divergence를 줄이는 문제가 두 Gaussian 평균 사이의 MSE를 줄이는 문제로 단순화된다. 이는 DDPM의 목적함수가 noise prediction MSE로 정리되는 배경 중 하나이다.

### 확인 문제

생성 모델이 다음 식을 최소화하는 이유를 설명해보자.

$$
-\log p_\theta(x)
$$

답:<br/>
$-\log p_\theta(x)$를 줄이면 $\log p_\theta(x)$가 커지고, 결과적으로 실제 데이터 $x$에 모델이 부여하는 확률 $p_\theta(x)$가 커지기 때문이다.
