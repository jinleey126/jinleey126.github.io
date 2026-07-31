---
title: "Diffusion U-Net의 Residual Block, Timestep Embedding과 Attention"
description: "Diffusion 모델의 noise predictor로 U-Net을 사용하는 이유와 residual block, timestep embedding, attention의 역할을 정리한다."
date: 2026-01-12 09:00:00 +0900
categories:
  - Paper Reviews
  - Multimodal
tags:
  - Diffusion
  - U-Net
  - Timestep Embedding
  - Attention
toc: true
math: true
---

## 0. 체크리스트

아래 질문들에 대해 답변할 수 있다면 해당 포스트는 바로 넘어가도 된다.

- Diffusion의 noise predictor로 U-Net을 사용하는 이유는 무엇인가?
- Residual block과 skip connection의 역할은 어떻게 다른가?
- 모델이 timestep $t$를 입력받아야 하는 이유는 무엇인가?
- Self-attention과 cross-attention은 각각 어떤 관계를 계산하는가?

---

## 1. 왜 U-Net인가?

Diffusion model의 입력 $x_t$와 출력 $\epsilon_\theta(x_t,t)$는 일반적으로 같은 공간 크기를 가진다.

$$
x_t\in\mathbb R^{C\times H\times W}
$$

$$
\epsilon_\theta(x_t,t)
\in
\mathbb R^{C\times H\times W}
$$

모델은 noisy image를 입력받아 각 위치에 포함된 noise를 예측해야 한다. 따라서 전체 이미지의 구조를 이해하는 동시에 픽셀 또는 latent 위치별 정보를 보존해야 한다.

U-Net은 여러 해상도에서 특징을 처리하면서 입력의 공간 정보를 유지하기 적합하다.

```text
noisy image
    ↓
downsampling blocks
    ↓
bottleneck
    ↓
upsampling blocks
    ↓
predicted noise
```

Downsampling path는 해상도를 줄이며 넓은 영역의 문맥을 추출한다. Upsampling path는 특징을 다시 원래 해상도로 복원한다.

<br/>

Down block의 feature는 같은 해상도의 up block으로 전달된다. 이를 U-Net skip connection이라고 한다.

- 깊은 층에서 손실되기 쉬운 위치 정보를 보존한다.
- 낮은 수준의 세부 특징과 높은 수준의 문맥을 결합한다.
- 출력이 입력과 같은 공간 구조를 갖도록 돕는다.

<br/>

## 2. Residual Block

Residual block은 다음 형태로 표현한다.

$$
y=x+F_\theta(x)
$$

네트워크가 전체 출력 $y$를 처음부터 만드는 대신 입력 $x$에 더할 변화량 $F_\theta(x)$를 학습한다.

이는 깊은 신경망에서 gradient가 전달될 수 있는 직접 경로를 제공해 최적화를 안정시킨다.

<br/>

Residual connection과 U-Net skip connection은 이름이 비슷하지만 역할과 연결 범위가 다르다.

| 구분 | Residual Connection | U-Net Skip Connection |
|---|---|---|
| 연결 범위 | 하나의 block 내부 | Down path와 Up path 사이 |
| 결합 방식 | 주로 덧셈 | 주로 channel 방향 concatenation |
| 주요 목적 | 최적화와 gradient 전달 안정화 | 공간 정보와 세부 특징 보존 |

<br/>

## 3. Timestep Embedding

동일한 $x_t$처럼 보이더라도 timestep에 따라 noise 수준과 필요한 denoising의 크기가 다르다. 따라서 모델은 이미지뿐 아니라 timestep $t$도 입력받아야 한다.

- 작은 $t$: 원본 신호가 많이 남아 있어 세부적인 noise 제거가 필요하다.
- 큰 $t$: 원본 신호가 적어 전체적인 구조 복원이 필요하다.

<br/>

Timestep은 일반적으로 sinusoidal embedding으로 변환한다.

$$
\operatorname{emb}(t)_{2i}
=
\sin\left(\frac{t}{\omega_i}\right)
$$

$$
\operatorname{emb}(t)_{2i+1}
=
\cos\left(\frac{t}{\omega_i}\right)
$$

이 embedding을 MLP에 통과시킨 뒤 각 residual block에 주입한다. 모델은 이를 통해 현재 입력의 noise level에 맞는 연산을 수행한다.

<br/>

## 4. Attention

Convolution은 주로 지역적인 특징을 처리한다. Self-attention은 이미지 또는 latent 내부의 멀리 떨어진 위치 사이 관계를 직접 계산한다.

$$
\operatorname{Attention}(Q,K,V)
=
\operatorname{softmax}
\left(
\frac{QK^\top}{\sqrt d}
\right)V
$$

각 요소의 역할은 다음과 같다.

- Query $Q$: 현재 위치가 찾고자 하는 정보
- Key $K$: 각 위치가 가진 정보의 기준
- Value $V$: attention weight에 따라 실제로 가져올 정보
- $\sqrt d$: dot product 크기를 조절하는 scaling factor

<br/>

Text-to-image Diffusion에서는 text condition을 반영하기 위해 cross-attention을 사용한다.

- Query: image latent feature
- Key, Value: text embedding

이를 통해 이미지의 각 위치가 prompt의 어떤 token을 참고할지 학습한다.

<br/>

## 5. 최소 미분방정식 지식

DDPM의 기본 학습 과정을 이해할 때 미분방정식이 필수는 아니다. 다만 SDE, probability-flow ODE와 flow matching으로 확장하려면 Euler method의 직관을 알아두는 것이 좋다.

다음 미분방정식을 생각해보자.

$$
\frac{dx}{dt}=f(x,t)
$$

작은 시간 간격 $\Delta t$에서 다음 상태를 Euler method로 근사하면 다음과 같다.

$$
x_{t+\Delta t}
\approx
x_t+f(x_t,t)\Delta t
$$

Sampling step을 잘게 나눌수록 작은 간격으로 생성 경로를 따라가는 것으로 이해할 수 있다.

<br/>

## 6. 미니 실습

다음 코드는 closed-form forward process를 이용해 $x_0$에서 $x_t$를 샘플링한다.

```python
import torch

x0 = torch.randn(16, 3, 32, 32)
epsilon = torch.randn_like(x0)

alpha_bar_t = torch.tensor(0.3)

xt = (
    alpha_bar_t.sqrt() * x0
    + (1 - alpha_bar_t).sqrt() * epsilon
)

print(x0.shape)
print(xt.mean(), xt.std())
```

`alpha_bar_t`를 다음 값으로 변경하며 결과를 관찰한다.

```python
0.99, 0.7, 0.3, 0.05, 0.001
```

$\bar\alpha_t$가 작아질수록 원본 신호의 비중은 줄고 $x_t$는 표준 Gaussian noise에 가까워진다.

### 확인 문제

Diffusion U-Net이 noisy image $x_t$만 입력받고 timestep $t$를 입력받지 않는다면 어떤 문제가 생기는지 설명해보자.

답:<br/>
모델은 현재 입력의 noise 수준을 알 수 없으므로 timestep에 맞는 denoising 강도를 선택하기 어렵다. Timestep embedding은 각 residual block이 현재 noise level에 맞는 특징 변환을 수행하도록 조건을 제공한다.
