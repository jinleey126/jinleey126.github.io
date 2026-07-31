---
title: "Diffusion 모델 학습을 위한 Latent Variable과 ELBO 기초"
description: "Diffusion 변분 추론 기초: Latent Variable · Likelihood · ELBO"
date: 2026-01-07 09:00:00 +0900
categories:
  - Paper Reviews
  - Multimodal
tags:
  - Diffusion
  - Latent Variable
  - ELBO
  - Variational Inference
toc: true
math: true
---

## 0. 체크리스트

아래 질문들에 대해 답변할 수 있다면 해당 포스트는 바로 넘어가도 된다.

- latent variable은 무엇인가?
- Diffusion에서 어떤 변수가 latent variable 역할을 하는가?
- $\log p_\theta(x_0)$를 직접 계산하기 어려운 이유는 무엇인가?
- ELBO를 크게 만드는 것은 무엇을 의미하는가?

---

## 1. Latent Variable

관측 데이터 $x$가 보이지 않는 변수 $z$를 거쳐 생성된다고 가정한다. 이때 $z$를 latent variable이라고 한다.

관측 데이터의 확률은 latent variable을 주변화하여 구한다.

$$
p_\theta(x)
=
\int p_\theta(x,z)\,dz
$$

VAE에서는 하나의 latent vector $z$를 사용한다. Diffusion에서는 원본 데이터 $x_0$에서 최종 noise $x_T$까지 이어지는 noisy trajectory가 latent variable 역할을 한다.

$$
x_1,x_2,\ldots,x_T
$$

즉, 관측되는 것은 $x_0$이지만 생성 과정 전체를 설명하려면 중간 상태 $x_{1:T}$를 함께 고려해야 한다.

<br/>

## 2. Diffusion의 Joint Distribution

Reverse process의 joint distribution은 다음처럼 분해한다.

$$
p_\theta(x_{0:T})
=
p(x_T)
\prod_{t=1}^{T}
p_\theta(x_{t-1}\mid x_t)
$$

각 항의 의미는 다음과 같다.

- $p(x_T)$: sampling을 시작하는 단순한 Gaussian prior
- $p_\theta(x_{t-1}\mid x_t)$: 한 단계 denoising을 수행하는 학습 가능한 reverse distribution
- $p_\theta(x_{0:T})$: 전체 reverse trajectory의 joint distribution

생성 과정은 $x_T\sim\mathcal N(0,I)$에서 시작해 $x_{T-1},\ldots,x_0$을 순서대로 샘플링한다.

<br/>

## 3. 왜 ELBO가 필요한가?

학습에서 직접 최대화하고 싶은 값은 원본 데이터의 log-likelihood이다.

$$
\log p_\theta(x_0)
$$

하지만 $p_\theta(x_0)$을 계산하려면 가능한 모든 latent trajectory $x_{1:T}$를 적분해야 한다.

$$
p_\theta(x_0)
=
\int
p_\theta(x_{0:T})
\,dx_{1:T}
$$

Diffusion의 timestep 수와 데이터 차원이 크기 때문에 이 적분을 직접 계산하기는 어렵다.

<br/>

따라서 계산 가능한 lower bound인 ELBO(Evidence Lower Bound)를 최적화한다.

$$
\log p_\theta(x_0)
\geq
\mathbb E_{q(x_{1:T}\mid x_0)}
\left[
\log
\frac{p_\theta(x_{0:T})}
{q(x_{1:T}\mid x_0)}
\right]
$$

오른쪽 항이 ELBO이다. ELBO를 크게 만들면 직접 계산하기 어려운 $\log p_\theta(x_0)$의 하한을 끌어올릴 수 있다.

<br/>

## 4. ELBO의 직관

ELBO를 크게 만드는 것은 다음 두 목표를 동시에 달성하는 과정이다.

- 모델이 실제 데이터 $x_0$에 높은 확률을 부여한다.
- 학습한 reverse process가 실제 forward posterior와 가까워진다.

DDPM에서는 negative ELBO를 timestep별 항으로 분해한다.

$$
\mathcal L
=
\mathcal L_T
+
\sum_{t=2}^{T}\mathcal L_{t-1}
+
\mathcal L_0
$$

중간 timestep의 항은 다음과 같은 KL divergence 형태를 가진다.

$$
\mathcal L_{t-1}
=
D_{\mathrm{KL}}
\left(
q(x_{t-1}\mid x_t,x_0)
\|
p_\theta(x_{t-1}\mid x_t)
\right)
$$

$q(x_{t-1}\mid x_t,x_0)$는 forward process로부터 계산할 수 있다. 따라서 모델은 $p_\theta(x_{t-1}\mid x_t)$가 이 분포와 가까워지도록 학습한다.

<br/>

Gaussian의 분산을 고정하면 KL divergence는 평균을 맞추는 문제로 단순화된다. 평균은 다시 예측 noise $\epsilon_\theta(x_t,t)$로 표현할 수 있으므로 최종적으로 noise prediction MSE를 사용할 수 있다.

```text
직접 likelihood 계산이 어려움
→ 계산 가능한 ELBO를 최대화
→ timestep별 reverse distribution을 맞추는 문제로 분해
→ Gaussian 평균을 맞추는 문제로 단순화
→ noise prediction MSE로 학습
```

### 확인 문제

ELBO가 log-likelihood의 lower bound라는 관계를 말로 설명해보자.

$$
\log p_\theta(x_0)
\geq
\operatorname{ELBO}(x_0)
$$

답:<br/>
원본 데이터의 log-likelihood는 latent trajectory 전체를 적분해야 하므로 직접 계산하기 어렵다. 대신 계산 가능한 ELBO를 크게 만들어 log-likelihood의 하한을 높이고, 모델이 데이터를 더 잘 설명하도록 학습한다.
